import os

from eval_model import eval_questions

import mesop as me

questions_dict = {q.name: q.question for q in eval_questions}


def get_all_files_in_gen_evals() -> list[str]:
  directory = "gen/eval/r1"
  files_list: list[str] = []
  for root, _, files in os.walk(directory):
    for file in files:
      files_list.append(os.path.join(root, file))
  return files_list


eval_files = get_all_files_in_gen_evals()


@me.page(path="/eval_app")
def page():
  with me.box(style=me.Style(margin=me.Margin.all(16))):
    me.text("Eval app")
    for f in eval_files:
      file_name = f.split("/")[-1]
      me.button(file_name, key=f, on_click=navigate_eval)


for file in eval_files:

  def create_page(file: str):
    @me.page(path="/eval_app/" + file.replace(".md", ""))
    def eval_page():
      with me.box(
        style=me.Style(margin=me.Margin.all(24), width="min(840px, 100%)")
      ):
        question_name = file.split("/")[-1].split(".")[0]
        with me.box(
          style=me.Style(
            background="lightblue",
            padding=me.Padding.all(16),
            border_radius=16,
          )
        ):
          me.text(questions_dict[question_name])
        with open(file) as f:
          me.markdown(
            f.read()
            # Simple hack to fix docs links.
            .replace(".md)", ")")
          )

  create_page(file)


def navigate_eval(e: me.ClickEvent):
  me.navigate("/eval_app/" + e.key.replace(".md", ""))
