from pathlib import Path
from uuid import uuid4

from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from openai import OpenAIError
from starlette.middleware.trustedhost import TrustedHostMiddleware

from secure_starter.advisor import Advisor, AdvisorResponseError, OpenAIAdvisor
from secure_starter.config import Settings, get_settings
from secure_starter.redaction import redact_text
from secure_starter.schemas import AssistRequest, AssistResponse, HealthResponse


def create_app(settings: Settings | None = None, advisor: Advisor | None = None) -> FastAPI:
    runtime = settings or get_settings()
    docs_enabled = runtime.app_env != "production"
    app = FastAPI(
        title=runtime.app_name,
        docs_url="/docs" if docs_enabled else None,
        redoc_url=None,
        openapi_url="/openapi.json" if docs_enabled else None,
    )
    app.add_middleware(TrustedHostMiddleware, allowed_hosts=runtime.trusted_hosts)

    if advisor is None and runtime.ai_configured:
        advisor = OpenAIAdvisor(runtime)
    app.state.advisor = advisor

    @app.middleware("http")
    async def security_headers(request: Request, call_next):
        request_id = uuid4().hex
        request.state.request_id = request_id
        response = await call_next(request)
        response.headers["Content-Security-Policy"] = (
            "default-src 'self'; base-uri 'none'; connect-src 'self'; "
            "form-action 'self'; frame-ancestors 'none'; object-src 'none'"
        )
        response.headers["Referrer-Policy"] = "no-referrer"
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-Frame-Options"] = "DENY"
        response.headers["Permissions-Policy"] = "camera=(), microphone=(), geolocation=()"
        response.headers["X-Request-ID"] = request_id
        return response

    @app.exception_handler(OpenAIError)
    @app.exception_handler(AdvisorResponseError)
    async def openai_error_handler(
        request: Request, _exc: OpenAIError | AdvisorResponseError
    ) -> JSONResponse:
        return JSONResponse(
            status_code=502,
            content={
                "detail": "The AI provider could not complete the request.",
                "request_id": request.state.request_id,
            },
        )

    @app.get("/api/health", response_model=HealthResponse)
    async def health() -> HealthResponse:
        return HealthResponse(ai_configured=runtime.ai_configured, environment=runtime.app_env)

    @app.post("/api/assist", response_model=AssistResponse)
    async def assist(payload: AssistRequest, request: Request) -> AssistResponse:
        active_advisor: Advisor | None = app.state.advisor
        if active_advisor is None:
            raise HTTPException(
                status_code=503,
                detail="AI is not configured. Add a local server-side key and restart.",
            )

        if len(payload.objective) + len(payload.context) > runtime.max_input_chars:
            raise HTTPException(status_code=413, detail="Input exceeds the configured limit.")

        objective = redact_text(payload.objective)
        context = redact_text(payload.context)
        result = await active_advisor.advise(
            mode=payload.mode,
            objective=objective.text,
            context=context.text,
        )
        return AssistResponse(
            advice=result.text,
            model=result.model,
            redactions_applied=objective.count + context.count,
            request_id=request.state.request_id,
        )

    static_root = Path(__file__).resolve().parents[2] / "static"
    app.mount("/", StaticFiles(directory=static_root, html=True), name="frontend")
    return app


app = create_app()
