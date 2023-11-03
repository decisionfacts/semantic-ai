import logging
import aiofiles
import json
from aiopath import AsyncPath

from df_extract.base import ImageExtract
from df_extract import pptx, pdf, docx, image, csv

from semantic_ai.utils import create_dir

logging.basicConfig(format='%(asctime)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

processed = 0
failed = 0
non_supported = 0

processed_files = f'processed_files.txt'
failed_files = f'failed_files.txt'
non_supported_files = f'non_supported_files.txt'
meta_file = f'meta.json'


async def update_meta(_dir):
    global processed
    global failed
    global non_supported
    meta = {
        "processed": processed,
        "failed": failed,
        "non_supported": non_supported
    }
    async with aiofiles.open(f"{_dir}/{meta_file}", 'w') as fobj:
        data = json.dumps(meta)
        await fobj.write(data)


async def _append_file_name(file_name, file_path):
    async with aiofiles.open(file_path, 'a') as fobj:
        await fobj.write(f'{file_name}\n')


async def add_processed_file(file_name, _dir):
    global processed
    await _append_file_name(file_name, f"{_dir}/{processed_files}")
    processed += 1
    await update_meta(_dir)


async def add_failed_file(file_name, _dir):
    global failed
    await _append_file_name(file_name, f"{_dir}/{failed_files}")
    failed += 1
    await update_meta(_dir)


async def add_non_supported_file(file_name, _dir):
    global non_supported
    await _append_file_name(file_name, f"{_dir}/{non_supported_files}")
    non_supported += 1
    await update_meta(_dir)


async def extract_content(
        path,
        output_dir,
        as_json: bool
):
    file_path = str(path)
    meta_path = await create_dir(output_dir, "meta")
    image_extract = ImageExtract(model_download_enabled=True)
    try:
        file_ext = path.suffix.lower()
        if file_ext in ('.pptx', '.ppt'):
            await pptx.ExtractPPTx(
                file_path=file_path,
                output_dir=output_dir,
                img_extract_obj=image_extract
            ).extract(as_json=as_json)
            await add_processed_file(file_path, meta_path)
        elif file_ext == '.docx':
            await docx.ExtractDocx(
                file_path=file_path,
                output_dir=output_dir,
                img_extract_obj=image_extract
            ).extract(as_json=as_json)
            await add_processed_file(file_path, meta_path)
        elif file_ext == ".pdf":
            await pdf.ExtractPDF(
                file_path=file_path,
                output_dir=output_dir,
                img_extract_obj=image_extract
            ).extract(as_json=as_json)
            await add_processed_file(file_path, meta_path)
        elif file_ext in (".png", '.jpg', '.jpeg'):
            await image.ExtractImage(
                file_path=file_path,
                output_dir=output_dir,
                img_extract_obj=image_extract
            ).extract(as_json=as_json)
            await add_processed_file(file_path, meta_path)
        elif file_ext == ".csv":
            await csv.ExtractCSV(
                file_path=file_path,
                output_dir=output_dir,
                image_extract=image_extract
            ).extract(as_json=as_json)
            await add_processed_file(file_path, meta_path)
        else:
            logger.info(f"{file_ext} is not supported")
            await add_non_supported_file(file_path, meta_path)
    except Exception as ex:
        await add_failed_file(file_path, meta_path)
        print(f"Error File---> {file_path}", ex)


async def extract(
        file_path: str,
        output_dir: str = None,
        as_json: bool = False
):
    input_path = AsyncPath(file_path)
    if await input_path.is_file():
        logger.info(f"Extraction processing")
        await extract_content(path=input_path,
                              output_dir=output_dir,
                              as_json=as_json)
        logger.info(f"Extraction completed")
    elif await input_path.is_dir():
        logger.info(f"Extraction processing")
        async for path in input_path.iterdir():
            if await path.is_file():
                await extract_content(path=path,
                                      output_dir=output_dir,
                                      as_json=as_json)
        logger.info(f"Extraction completed")
    else:
        logger.info(f"{input_path} is unsupported")
