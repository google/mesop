import mesop as me


def load(e: me.LoadEvent):
  me.set_theme_mode("system")


@me.page(
  on_load=load,
  security_policy=me.SecurityPolicy(
    allowed_iframe_parents=["https://mesop-dev.github.io"],
  ),
  path="/card",
)
def app():
  with me.box(
    style=me.Style(
      display="flex",
      flex_direction="column",
      gap=15,
      margin=me.Margin.all(15),
      max_width=500,
    )
  ):
    with me.card(appearance="outlined"):
      me.card_header(
        title="Grapefruit",
        subtitle="Kind of fruit",
        image="https://interactive-examples.mdn.mozilla.net/media/cc0-images/grapefruit-slice-332-332.jpg",
      )
      me.image(
        style=me.Style(
          width="100%",
        ),
        src="https://interactive-examples.mdn.mozilla.net/media/cc0-images/grapefruit-slice-332-332.jpg",
      )
      with me.card_content():
        me.text(
          "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nulla sed augue ultricies, laoreet nunc eget, ultricies augue. In ornare bibendum mauris vel sodales. Donec ut interdum felis. Nulla facilisi. Morbi a laoreet turpis, sed posuere arcu. Nam nisi neque, molestie vitae euismod eu, sollicitudin eu lectus. Pellentesque orci metus, finibus id faucibus et, ultrices quis dui. Duis in augue ac metus tristique lacinia."
        )

      with me.card_actions(align="end"):
        me.button(label="Add to cart")
        me.button(label="Buy")

    with me.card(appearance="raised"):
      me.card_header(
        title="Grapefruit",
        subtitle="Kind of fruit",
        image="https://interactive-examples.mdn.mozilla.net/media/cc0-images/grapefruit-slice-332-332.jpg",
        image_type="small",
      )

      with me.card_content():
        me.text(
          "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nulla sed augue ultricies, laoreet nunc eget, ultricies augue. In ornare bibendum mauris vel sodales. Donec ut interdum felis. Nulla facilisi. Morbi a laoreet turpis, sed posuere arcu. Nam nisi neque, molestie vitae euismod eu, sollicitudin eu lectus. Pellentesque orci metus, finibus id faucibus et, ultrices quis dui. Duis in augue ac metus tristique lacinia."
        )

      with me.card_actions(align="start"):
        me.button(label="Add to cart")
        me.button(label="Buy")

    with me.card(appearance="outlined"):
      me.card_header(
        title="Grapefruit",
        subtitle="Kind of fruit",
        image="https://interactive-examples.mdn.mozilla.net/media/cc0-images/grapefruit-slice-332-332.jpg",
        image_type="medium",
      )

      with me.card_content():
        me.text(
          "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nulla sed augue ultricies, laoreet nunc eget, ultricies augue. In ornare bibendum mauris vel sodales. Donec ut interdum felis. Nulla facilisi. Morbi a laoreet turpis, sed posuere arcu. Nam nisi neque, molestie vitae euismod eu, sollicitudin eu lectus. Pellentesque orci metus, finibus id faucibus et, ultrices quis dui. Duis in augue ac metus tristique lacinia."
        )

      with me.card_actions(align="start"):
        me.button(label="Add to cart")
        me.button(label="Buy")

      me.card_header(
        title="Grapefruit",
        image="https://interactive-examples.mdn.mozilla.net/media/cc0-images/grapefruit-slice-332-332.jpg",
        image_type="large",
      )

      with me.card_content():
        me.text(
          "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nulla sed augue ultricies, laoreet nunc eget, ultricies augue. In ornare bibendum mauris vel sodales. Donec ut interdum felis. Nulla facilisi. Morbi a laoreet turpis, sed posuere arcu. Nam nisi neque, molestie vitae euismod eu, sollicitudin eu lectus. Pellentesque orci metus, finibus id faucibus et, ultrices quis dui. Duis in augue ac metus tristique lacinia."
        )

      with me.card_actions(align="end"):
        me.button(label="Add to cart")
        me.button(label="Buy")

      me.card_header(
        title="Grapefruit",
        image_type="large",
      )

      with me.card_content():
        me.text(
          "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nulla sed augue ultricies, laoreet nunc eget, ultricies augue. In ornare bibendum mauris vel sodales. Donec ut interdum felis. Nulla facilisi. Morbi a laoreet turpis, sed posuere arcu. Nam nisi neque, molestie vitae euismod eu, sollicitudin eu lectus. Pellentesque orci metus, finibus id faucibus et, ultrices quis dui. Duis in augue ac metus tristique lacinia."
        )
