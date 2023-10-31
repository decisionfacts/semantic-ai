from aiopath import AsyncPath

from df_extract.base import ImageExtract
from df_extract import pptx, pdf, docx, image, csv

image_extract = ImageExtract(model_download_enabled=True)


async def extract_content(path, output_dir, as_json: bool):
    file_path = str(path)
    try:
        file_ext = path.suffix.lower()
        if file_ext in ('.pptx', '.ppt'):
            await pptx.ExtractPPTx(
                file_path=file_path,
                output_dir=output_dir,
                img_extract_obj=image_extract
            ).extract(as_json=as_json)
        elif file_ext == '.docx':
            await docx.ExtractDocx(
                file_path=file_path,
                output_dir=output_dir,
                img_extract_obj=image_extract
            ).extract(as_json=as_json)
        elif file_ext == ".pdf":
            await pdf.ExtractPDF(
                file_path=file_path,
                output_dir=output_dir,
                img_extract_obj=image_extract
            ).extract(as_json=as_json)
        elif file_ext in (".png", '.jpg', '.jpeg'):
            await image.ExtractImage(
                file_path=file_path,
                output_dir=output_dir,
                img_extract_obj=image_extract
            ).extract(as_json=as_json)
        elif file_ext == ".csv":
            await csv.ExtractCSV(
                file_path=file_path,
                output_dir=output_dir,
                image_extract=image_extract
            ).extract(as_json=as_json)
        else:
            print(f"{file_ext} is not supported")
    except Exception as ex:
        print(f"Error File---> {file_path}", ex)


async def extract(file_path: str, output_dir: str = None, as_json: bool = False):
    input_path = AsyncPath(file_path)
    if await input_path.is_file():
        await extract_content(path=input_path,
                              output_dir=output_dir,
                              as_json=as_json)
    elif await input_path.is_dir():
        async for path in input_path.iterdir():
            if await path.is_file():
                await extract_content(path=path,
                                      output_dir=output_dir,
                                      as_json=as_json)
    else:
        print(f"{input_path} is unsupported")
