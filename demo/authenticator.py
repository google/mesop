import mesop as me

@me.stateclass
class State:
    username: str = ""
    password: str = ""
    welcome_message: str = ""
    error_message: str = ""

def on_blur_username(e: me.InputBlurEvent):
    state = me.state(State)
    state.username = e.value

def on_blur_password(e: me.InputBlurEvent):
    state = me.state(State)
    state.password = e.value

def on_login(e: me.ClickEvent):
    state = me.state(State)
    
    # Validate username and password
    if not state.username or not state.password:
        state.error_message = "Please enter both username and password."
        return
    
    # Simulate a simple login check (replace with actual authentication logic)
    # Here, you can replace this with your own authentication logic.
    # For demonstration purposes, any non-empty username and password will be accepted.
    if state.username and state.password:
        state.welcome_message = f"Welcome, {state.username}!"
        state.error_message = ""  # Clear any previous error message
        me.navigate("/welcome")  # Navigate to the welcome page after successful login
    else:
        state.error_message = "Incorrect username or password."
    
    # Clear the username and password fields
    state.username = ""
    state.password = ""

@me.page(
    security_policy=me.SecurityPolicy(
        allowed_iframe_parents=["https://google.github.io"]
    ),
    path="/login",
)
def app():
    s = me.state(State)
    
    with me.box(
        style=me.Style(
            display="flex",
            flex_direction="column",
            align_items="center",
            justify_content="center",
            height="100vh",
            background="white",
        )
    ):
        me.text("Authenticator", style=me.Style(font_size=24, margin=me.Margin(bottom=16)))
        
        if s.error_message:
            me.text(s.error_message, style=me.Style(color="red", margin=me.Margin(bottom=8)))
        
        with me.box(
            style=me.Style(
                background="white",
                padding=me.Padding.all(16),
                margin=me.Margin.symmetric(vertical=24, horizontal=12),
                border=me.Border.all(me.BorderSide(width=2, color="gray", style="solid")),
                border_radius=10,
                width="300px",
            )
        ):
            with me.box(
                style=me.Style(
                    background="white",
                    margin=me.Margin.symmetric(vertical=8),
                )
            ):
                me.input(label="Username", value=s.username, on_blur=on_blur_username, style=me.Style(width="100%"))
            with me.box(
                style=me.Style(
                    background="white",
                    margin=me.Margin.symmetric(vertical=8),
                )
            ):
                me.input(label="Password", type="password", value=s.password, on_blur=on_blur_password, style=me.Style(width="100%"))
            with me.box(
                style=me.Style(
                    background="white",
                    margin=me.Margin.symmetric(vertical=8),
                )
            ):
                me.button(label="Login", on_click=on_login)

@me.page(
    path="/welcome"
)
def welcome_page():
    s = me.state(State)
    if s.welcome_message:
        me.text(s.welcome_message)
