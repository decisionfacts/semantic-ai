from aiopath import AsyncPath

from df_extract.base import ImageExtract
from df_extract import pptx, pdf, docx, image, csv

image_extract = ImageExtract(model_download_enabled=True)


class Extract:

    def __init__(
            self,
            file_path: str,
            output_dir: str = None,
            as_json: bool = False
    ):
        self.file_path = file_path
        self.output_dir = output_dir
        self.as_json = as_json

    async def extract_content(self, path):
        file_path = str(path)
        try:
            file_ext = path.suffix.lower()
            if file_ext in ('.pptx', '.ppt'):
                await pptx.ExtractPPTx(
                    file_path=file_path,
                    output_dir=self.output_dir,
                    img_extract_obj=image_extract
                ).extract(as_json=self.as_json)
            elif file_ext == '.docx':
                await docx.ExtractDocx(
                    file_path=file_path,
                    output_dir=self.output_dir,
                    img_extract_obj=image_extract
                ).extract(as_json=self.as_json)
            elif file_ext == ".pdf":
                await pdf.ExtractPDF(
                    file_path=file_path,
                    output_dir=self.output_dir,
                    img_extract_obj=image_extract
                ).extract(as_json=self.as_json)
            elif file_ext in (".png", '.jpg', '.jpeg'):
                await image.ExtractImage(
                    file_path=file_path,
                    output_dir=self.output_dir,
                    img_extract_obj=image_extract
                ).extract(as_json=self.as_json)
            elif file_ext == ".csv":
                await csv.ExtractCSV(
                    file_path=file_path,
                    output_dir=self.output_dir,
                    image_extract=image_extract
                ).extract(as_json=self.as_json)
            else:
                print(f"{file_ext} is not supported")
        except Exception as ex:
            print(f"Error File---> {file_path}", ex)

    async def extract(self):
        input_path = AsyncPath(self.file_path)
        if await input_path.is_file():
            await self.extract_content(input_path)
        elif await input_path.is_dir():
            async for path in input_path.iterdir():
                if await path.is_file():
                    await self.extract_content(path)
        else:
            pass
