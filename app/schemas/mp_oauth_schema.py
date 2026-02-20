from pydantic import BaseModel


class MPOAuthCallbackRequest(BaseModel):
    """Schema para recibir el code, state y code_verifier del callback de MP OAuth."""

    code: str
    state: str  # seller_id que se envió como state
    code_verifier: str  # PKCE code_verifier generado al iniciar el flujo


class MPOAuthTokenResponse(BaseModel):
    """Respuesta al vincular exitosamente la cuenta de MP."""

    message: str
    mp_user_id: int


class MPAuthURLResponse(BaseModel):
    """URL de autorización de MP y code_verifier para el frontend."""

    auth_url: str
    code_verifier: str  # El frontend debe guardarlo y enviarlo en el callback
