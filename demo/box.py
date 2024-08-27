# import mesop as me


# @me.page(
#   security_policy=me.SecurityPolicy(
#     allowed_iframe_parents=["https://google.github.io"]
#   ),
#   path="/box",
# )
# def app():
#   with me.box(style=me.Style(background=me.theme_var("background"), padding=me.Padding.all(16))):
#     with me.box(
#       style=me.Style(
#         background=me.theme_var("surface-variant"),
#         padding=me.Padding.all(16),
#         margin=me.Margin(bottom=24),
#         border=me.Border.all(
#           me.BorderSide(width=1, color=me.theme_var("outline"), style="solid")
#         ),
#         border_radius=8,
#         box_shadow="0 2px 4px rgba(0, 0, 0, 0.1)",
#       )
#     ):
#       me.text(
#         text="Welcome to the Box Examples",
#         style=me.Style(
#           font_weight="bold",
#           font_size=24,
#           color=me.theme_var("on-surface-variant"),
#           margin=me.Margin(bottom=8),
#         )
#       )
#       me.text(
#         text="Explore different box styles and borders to enhance your application's UI.",
#         style=me.Style(
#           font_weight="medium",
#           font_size=16,
#           color=me.theme_var("on-surface-variant"),
#         )
#       )

#     with me.box(
#       style=me.Style(
#         background="green",
#         height=50,
#         margin=me.Margin.symmetric(vertical=24, horizontal=12),
#         border=me.Border.symmetric(
#           horizontal=me.BorderSide(width=2, color="pink", style="solid"),
#           vertical=me.BorderSide(width=2, color="orange", style="solid"),
#         ),
#       )
#     ):
#       me.text(text="hi1")
#       me.text(text="hi2")

#     # <--- EDIT HERE
# # <--- EDIT HERE
# with me.box(
#       style=me.Style(
#         background=me.theme_var("primary"),
#         height=60,
#         margin=me.Margin.all(16),
#         border=me.Border.all(
#           me.BorderSide(width=2, color=me.theme_var("primary-variant"), style="solid")
#         ),
#         border_radius=12,
#         display="flex",
#         align_items="center",
#         justify_content="center",
#         box_shadow="0 4px 6px rgba(0, 0, 0, 0.1)",
#         transition="background-color 0.3s, transform 0.2s",
#       )
#     ):
#       with me.box(
#         style=me.Style(
#           padding=me.Padding.all(12),
#           border=me.Border.all(
#             me.BorderSide(width=2, color=me.theme_var("surface"), style="solid")
#           ),
#           border_radius=8,
#         )
#       ):
#         me.text(
#           text="Example with all sides bordered",
#           style=me.Style(
#             font_weight="bold",
#             font_size=18,
#             color=me.theme_var("on-primary"),
#             text_align="center",
#           )
#         )

#     with me.box(
#       style=me.Style(
#         background=me.theme_var("primary"),
#         height=60,
#         margin=me.Margin.all(16),
#         border=me.Border.all(
#           me.BorderSide(width=2, color=me.theme_var("primary-variant"), style="solid")
#         ),
#         border_radius=12,
#         display="flex",
#         align_items="center",
#         justify_content="center",
#         box_shadow="0 4px 6px rgba(0, 0, 0, 0.1)",
#         transition="background-color 0.3s, transform 0.2s",
#       )
#     ):
#       with me.box(
#         style=me.Style(
#           padding=me.Padding.all(12),
#           border=me.Border.all(
#             me.BorderSide(width=2, color=me.theme_var("surface"), style="solid")
#           ),
#           border_radius=8,
#         )
#       ):
#         me.text(
#           text="Newly added box with consistent theme"
#           style=me.Style(
#             font_weight="bold",
#             font_size=18,
#             color=me.theme_var("on-primary"),
#             text_align="center",
#           )
#         )

#     with me.box(
#       style=me.Style(
#         background=me.theme_var("primary"),
#         height=60,
#         margin=me.Margin.all(16),
#         border=me.Border.all(
#           me.BorderSide(width=2, color=me.theme_var("primary-variant"), style="solid")
#         ),
#         border_radius=12,
#         display="flex",
#         align_items="center",
#         justify_content="center",
#         box_shadow="0 4px 6px rgba(0, 0, 0, 0.1)",
#         transition="background-color 0.3s, transform 0.2s",
#       )
#     ):
#       with me.box(
#         style=me.Style(
#           padding=me.Padding.all(12),
#           border=me.Border.all(
#             me.BorderSide(width=2, color=me.theme_var("surface"), style="solid")
#           ),
#           border_radius=8,
#         )
#       ):
#         me.text(
#           text="Newly added box with consistent theme"
#           style=me.Style(
#             font_weight="bold",
#             font_size=18,
#             color=me.theme_var("on-primary"),
#             text_align="center",
#           )
#         )

#     with me.box(
#       style=me.Style(
#         background="purple",
#         height=50,
#         margin=me.Margin.symmetric(vertical=24, horizontal=12),
#         border=me.Border.symmetric(
#           vertical=me.BorderSide(width=4, color="white", style="double")
#         ),
#       )
#     ):
#       me.text(text="Example with top and bottom borders")

#     with me.box(
#       style=me.Style(
#         background=me.theme_var("surface"),
#         padding=me.Padding.all(16),
#         margin=me.Margin.symmetric(vertical=24, horizontal=12),
#         border=me.Border.all(
#           me.BorderSide(width=1, color=me.theme_var("outline"), style="solid")
#         ),
#         border_radius=8,
#         box_shadow="0 2px 4px rgba(0, 0, 0, 0.1)",
#       )
#     ):
#       with me.box(
#         style=me.Style(
#           display="flex",
#           align_items="center",
#           gap=8,
#         )
#       ):
#         me.icon("border_left")  # Add an icon to enhance visual communication
#         me.text(
#           text="Example with left and right borders",
#           style=me.Style(
#             font_weight="medium",
#             font_size=16,
#             color=me.theme_var("on-surface")
#           )
#         )
