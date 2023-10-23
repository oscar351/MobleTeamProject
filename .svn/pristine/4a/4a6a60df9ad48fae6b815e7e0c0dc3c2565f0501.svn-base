# -*- coding: utf-8 -*-

from PyPDF2 import PdfReader
from pdf2image import convert_from_path
import os
import re
import typing
from common.logManage import logManage
from common.commonService import commonService

logs = logManage()  # 사용자 관리 API 로그를 남기기 위한 객체 할당


class pdfService:
    """pdf 이미지 변환 서비스 class"""

    def preprocess_title(self, raw_title: str):
        """원시 제목을 도면코드와 도면제목으로 분리한다"""
        raw_title = raw_title.strip()

        # 도면 코드 추출
        code, title = re.split(" ", raw_title, maxsplit=1)

        # 뒷 부분 제거
        title = re.sub("[a-zA-Z]+ +[0-9()]+", "", title)

        title = title.strip()

        # subpage 추출
        subpage = 0
        raw_subpage = re.findall("- *\d+", title)
        subcheck = re.findall("확대", title)
        if raw_subpage and subcheck:
            subpage = int(re.sub("[^0-9]", "", raw_subpage[0]))

        return subpage, code, title

    def extract_bookmarks(self, pdf_reader: PdfReader):
        """pdf 파일의 북마크 정보를 추출한다"""
        outlines = pdf_reader.outline
        subpages, codes, titles = list(), list(), list()

        # 북마크 페이지 제목이 PDF 페이지 수보다 적으면 변환 불가능한 파일로 인식한다
        if len(outlines) < len(pdf_reader.pages):
            raise ValueError("북마크를 읽을 수 없습니다")

        # 북마크 정보에서 각 페이지 제목을 가져온다
        for outline in outlines:
            raw_title = outline["/Title"]
            subpage, code, title = self.preprocess_title(raw_title)
            subpages.append(subpage)
            codes.append(code)
            titles.append(title)

        return subpages, codes, titles

    def pdf2image(self, file_name: str):
        """pdf를 읽어 이미지 리스트로 반환한다"""

        commServ = commonService()

        # 파일을 읽어들인다
        pdf_reader = PdfReader(file_name)
        num_pages = len(pdf_reader.pages)
        folder, _ = os.path.splitext(file_name)
        commServ.createDir(folder)

        # 북마크 정보를 추출한다
        subpages, codes, titles = self.extract_bookmarks(pdf_reader)

        # 기본 쓰레드 수로 20페이지씩 이미지 변환을 시도한다
        for page in range(1, num_pages + 1, 20):
            images = convert_from_path(
                file_name,
                dpi=200,
                fmt="jpeg",
                thread_count=4,
                grayscale=True,
                first_page=page,
                last_page=min(page + 19, num_pages),
            )

            pages = range(page, min(page + 19, num_pages) + 1)
            for image, page in zip(images, pages):
                image.save("{}/{}.jpg".format(folder, page), "JPEG")

        pages = range(1, num_pages + 1)
        return pages, subpages, codes, titles

    def raw_pdf2image(self, file_name: str) -> None:
        """pdf를 읽어 컬러이미지로 저장만 한다"""
        commServ = commonService()

        # 파일을 읽어들인다
        pdf_reader = PdfReader(file_name)
        num_pages = len(pdf_reader.pages)
        folder, _ = os.path.splitext(file_name)
        commServ.createDir(folder)

        # 기본 쓰레드 수로 20페이지씩 이미지 변환을 시도한다 [1 - num_pages]
        for page in range(1, num_pages + 1, 20):
            images = convert_from_path(
                file_name,
                dpi=200,
                fmt="jpeg",
                thread_count=4,
                first_page=page,
                last_page=min(page + 19, num_pages),
            )

            pages = range(page, min(page + 19, num_pages) + 1)
            for image, page in zip(images, pages):
                image.save("{}/{}.jpg".format(folder, page), "JPEG")

        pages = range(1, num_pages + 1)
        return
