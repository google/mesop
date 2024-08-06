from dataclasses import dataclass

import mesop as me

CARD_WIDTH = "320px"


def scroll_to_section(e: me.ClickEvent):
  me.scroll_into_view(key="section-" + e.key)


def toggle_theme(e: me.ClickEvent):
  if me.theme_brightness() == "light":
    me.set_theme_mode("dark")
  else:
    me.set_theme_mode("light")


@me.page(
  path="/showcase",
  title="Mesop Showcase",
)
def page():
  with me.box(style=me.Style(display="flex", height="100%")):
    with me.box(
      style=me.Style(
        width=240,
        height="100%",
        background=me.theme_var("surface-container-low"),
        padding=me.Padding.all(16),
      )
    ):
      with me.box(
        style=me.Style(
          padding=me.Padding(top=48),
          display="flex",
          flex_direction="column",
          gap=16,
        ),
      ):
        me.text(
          "Categories",
          style=me.Style(
            font_weight=500,
            letter_spacing="0.4px",
            padding=me.Padding(left=12),
          ),
        )
        for section in SECTIONS:
          with me.box(
            style=me.Style(
              display="flex",
              align_items="center",
              cursor="pointer",
            ),
            on_click=scroll_to_section,
            key=section.name,
          ):
            with me.content_button(type="icon"):
              me.icon(section.icon)
            me.text(section.name)
    with me.box(
      style=me.Style(
        background=me.theme_var("surface-container-low"),
        display="flex",
        flex_direction="column",
        flex_grow=1,
      )
    ):
      with me.box(
        style=me.Style(
          height=80,
          width="100%",
          padding=me.Padding.all(16),
        ),
      ):
        me.text(
          "Mesop Showcase",
          style=me.Style(
            color=me.theme_var("on-background"),
            font_size=18,
            font_weight=500,
            letter_spacing="0.8px",
          ),
        )

        with me.content_button(
          type="icon",
          style=me.Style(position="absolute", right=4, top=8),
          on_click=toggle_theme,
        ):
          me.icon(
            "light_mode" if me.theme_brightness() == "dark" else "dark_mode"
          )
      with me.box(
        style=me.Style(
          background=me.theme_var("background"),
          flex_grow=1,
          padding=me.Padding(
            left=32,
            right=32,
            bottom=64,
          ),
          border_radius=16,
          overflow_y="auto",
        )
      ):
        for section in SECTIONS:
          me.text(
            section.name,
            style=me.Style(
              font_size=18,
              font_weight=500,
              padding=me.Padding(top=32, bottom=16),
            ),
            key="section-" + section.name,
          )
          with me.box(
            style=me.Style(
              display="grid",
              grid_template_columns=f"repeat(auto-fit, minmax({CARD_WIDTH}, 1fr))",
              gap=24,
              margin=me.Margin(
                bottom=24,
              ),
            )
          ):
            for resource in section.resources:
              card(resource)


@dataclass
class Resource:
  title: str
  description: str
  github_url: str
  github_username: str
  img_url: str
  app_url: str | None = None


@dataclass
class Section:
  name: str
  resources: list[Resource]
  icon: str


SECTIONS = [
  Section(
    name="Featured",
    icon="star",
    resources=[
      Resource(
        title="Mesop Duo Chat",
        description="Chat with multiple models at once",
        github_url="https://github.com/wwwillchen/mesop-duo-chat",
        github_username="wwwillchen",
        app_url="https://huggingface.co/spaces/wwwillchen/mesop-duo-chat",
        img_url="https://github.com/user-attachments/assets/107afb9c-f08c-4f27-bd00-e122415c069e",
      ),
      Resource(
        title="Mesop Prompt Tuner",
        description="Prompt tuning app heavily inspired by Anthropic Console Workbench.",
        app_url="https://huggingface.co/spaces/richard-to/mesop-prompt-tuner",
        img_url="https://github.com/user-attachments/assets/2ec6cbfb-c28b-4f60-98f9-34bfca1f6938",
        github_url="https://github.com/richard-to/mesop-prompt-tuner",
        github_username="richard-to",
      ),
      Resource(
        title="Meta Llama Agentic System",
        description="Agentic components of the Llama Stack APIs. Chat UI in Mesop.",
        img_url="https://github.com/meta-llama/llama-agentic-system/raw/main/demo.png",
        github_url="https://github.com/meta-llama/llama-agentic-system",
        github_username="meta-llama",
      ),
    ],
  ),
  Section(
    name="Apps",
    icon="computer",
    resources=[
      Resource(
        title="Mesop App Maker",
        description="Generate apps with Mesop using LLMs",
        img_url="https://github.com/user-attachments/assets/1a826d44-c87b-4c79-aeaf-29bc8da3b1c0",
        github_url="https://github.com/richard-to/mesop-app-maker",
        github_username="richard-to",
      ),
      Resource(
        title="Mesop Jeopardy",
        description="A simple jeopardy game built using Mesop",
        img_url="https://github.com/richard-to/mesop-jeopardy/assets/539889/bc27447d-129f-47ae-b0b1-8f5c546762ed",
        github_url="https://github.com/richard-to/mesop-jeopardy",
        github_username="richard-to",
      ),
    ],
  ),
  Section(
    name="Web components",
    icon="code_blocks",
    resources=[
      Resource(
        title="Mesop Markmap",
        description="Mesop web component for the Markmap library",
        img_url="https://github.com/user-attachments/assets/6aa40ca3-d98a-42b2-adea-3f49b134445d",
        github_url="https://github.com/lianggecm/mesop_markmap",
        app_url="https://colab.research.google.com/drive/17gXlsXPDeo6hcFl1oOyrZ58FTozviN45?usp=sharing",
        github_username="lianggecm",
      ),
    ],
  ),
  Section(
    name="Notebooks",
    icon="description",
    resources=[
      Resource(
        title="Mesop Getting Started Colab",
        description="Get started with Mesop in Colab",
        img_url="https://github.com/user-attachments/assets/37efbe69-ac97-4d26-8fda-d1b7b2b4976a",
        github_url="https://github.com/google/mesop/blob/main/notebooks/mesop_colab_getting_started.ipynb",
        app_url="https://colab.research.google.com/github/google/mesop/blob/main/notebooks/mesop_colab_getting_started.ipynb",
        github_username="google",
      ),
      Resource(
        title="Gemma with Mesop Notebook",
        description="Use Gemma with Mesop in Colab",
        img_url="https://github.com/user-attachments/assets/a52ebf01-7f24-469b-9ad9-b271fdb19e37",
        github_url="https://github.com/google-gemini/gemma-cookbook/blob/main/Gemma/Integrate_with_Mesop.ipynb",
        app_url="https://colab.research.google.com/github/google-gemini/gemma-cookbook/blob/main/Gemma/Integrate_with_Mesop.ipynb",
        github_username="google-gemini",
      ),
      Resource(
        title="PaliGemma with Mesop Notebook",
        description="Use PaliGemma with Mesop in Colab",
        img_url="https://github.com/user-attachments/assets/8cb456a1-f7be-4187-9a3f-f6b48bde73e9",
        github_url="https://github.com/google-gemini/gemma-cookbook/blob/main/PaliGemma/Integrate_PaliGemma_with_Mesop.ipynb",
        app_url="https://colab.research.google.com/github/google-gemini/gemma-cookbook/blob/main/PaliGemma/Integrate_PaliGemma_with_Mesop.ipynb",
        github_username="google-gemini",
      ),
    ],
  ),
]


def card(resource: Resource):
  with me.box(
    style=me.Style(
      display="flex",
      flex_direction="column",
      gap=12,
      box_shadow="0 2px 4px rgba(0, 0, 0, 0.1)",
      border_radius=16,
      min_width=CARD_WIDTH,
      max_width=480,
      background=me.theme_var("surface-container-lowest"),
    )
  ):
    me.box(
      style=me.Style(
        background=f"url('{resource.img_url}') center/cover no-repeat",
        height=200,
        width="100%",
        border_radius=16,
        margin=me.Margin(bottom=8),
      )
    )
    # me.image(src=resource.img_url, style=me.Style(width="100%"))
    with me.box(
      style=me.Style(
        padding=me.Padding(left=16),
        display="flex",
        flex_direction="column",
        gap=8,
      )
    ):
      me.text(resource.title, style=me.Style(font_weight="bold"))
      with me.box(
        style=me.Style(
          display="flex",
          flex_direction="row",
          align_items="center",
          gap=8,
          cursor="pointer",
        )
      ):
        me.image(
          src="https://avatars.githubusercontent.com/"
          + resource.github_username,
          style=me.Style(height=32, width=32, border_radius=16),
        )
        me.text(
          resource.github_username,
          style=me.Style(
            letter_spacing="0.2px",
          ),
        )
      me.text(resource.description, style=me.Style(height=40))
    with me.box(
      style=me.Style(
        display="flex",
        justify_content="space-between",
        padding=me.Padding(left=8, right=8, bottom=8),
      )
    ):
      me.button("Open repo")
      if resource.app_url:
        me.button("Open app")
