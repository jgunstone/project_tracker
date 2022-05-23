"""
generate a templated project summary from user input form
"""
import pathlib
import pandas as pd
from jinja2 import Environment, FileSystemLoader
from input_schema_project import Project
from docx_to_pdf import docx_to_pdf


DIR_CORE = pathlib.Path(__file__).parent
FDIR_TEMPLATES = DIR_CORE / "templates"
NAME_JINJA_PROJECT = "project.jinja"
FPTH_REFERENCE_DOCX = DIR_CORE / "templates" / 'default_refdocx_nofrontpage.docx'

def make_table(di, name="Brief"):
    df = pd.DataFrame.from_dict({k: [v] for k, v in di[name].items()}).T.reset_index()
    df.columns = [name, ""]
    df = df.set_index(name)
    return df.to_markdown(tablefmt="grid")


def make_tables(di):
    di_ = {}
    for k, v in di.items():
        if isinstance(v, dict) and k != "Linked Files":
            di_[k] = make_table(di, k)
    return di_


def get_summary(pr):
    di = pr.dict(by_alias=False)
    if di["current_status"] is not None:
        di["current_status"] = di["current_status"].upper()
    li = ["project_name", "project_summary", "current_status"]

    return {k: v for k, v in di.items() if k in li}


def prepare_jinja(pr):
    di_summary = get_summary(pr)
    di_tables = make_tables(pr.dict(by_alias=True))
    di = di_summary | di_tables
    return di



def main(fpth_in, fpth_out_md, fpth_out_docx, fpth_out_pdf):
    file_loader = FileSystemLoader(FDIR_TEMPLATES)
    env = Environment(loader=file_loader)
    template = env.get_template(NAME_JINJA_PROJECT)

    pr = Project.parse_file(fpth_in)
    pr.dict(by_alias=False)

    di = prepare_jinja(pr)
    render = template.render(**di)
    fpth_out_md.write_text(render)
    fpth_out_docx = fpth_out_md.with_suffix(".docx")
    fpth_out_pdf = fpth_out_md.with_suffix(".pdf")
    cmd=f'pandoc {fpth_out_md} -s -f markdown -t docx -o {fpth_out_docx} --reference-doc={FPTH_REFERENCE_DOCX}'
    #docx_to_pdf(fpth_out_docx, fpth_out_pdf) # TODO: make this work

    
if __name__ == "__main__":
    if __debug__:
        pass
    else:
        import sys
        fpth_in = pathlib.Path(sys.argv[1])
        fpth_out_md = pathlib.Path(sys.argv[2])
        fpth_out_docx = pathlib.Path(sys.argv[3])
        fpth_out_pdf = pathlib.Path(sys.argv[4])
        print(f"fpth_in = {str(fpth_in)}")
        print(f"fpth_out_md = {str(fpth_out_md)}")
        print(f"fpth_out_pdf = {str(fpth_out_pdf)}")
        main(fpth_in, fpth_out_md, fpth_out_docx, fpth_out_pdf)