# _*_coding: utf-8 -*-

from common.commUtilService import commUtilService


SELECT_MATERIALMANAGE_INFO = """SELECT
									A.MATERIAL_NUM AS material_num,
									A.MATERIAL_NAME AS material_name,
									IFNULL(A.STANDARD, '') AS standard,
									IFNULL(A.UNIT, '') AS unit,
									A.PRODUCE_CO AS produce_co,
									IFNULL(A.APPROVAL_NUM, '') AS approval_num,
									IFNULL(A.APPROVAL_DATE, '') AS approval_date,
									IFNULL(A.TYPE, '') AS type,
									IFNULL(A.FORMAL_NAME, '') AS formal_name,
									IFNULL(A.NOTE, '') AS note,
									A.KS_WHETHER AS ks_whether,
									A.COLLECT_TYPE AS collect_type,
									IFNULL(A.UPDATE_DATE, '') AS update_date,
									IFNULL(A.KS_PERMIT_COPY_PATH, '') AS ks_permit_copy_path,
									IFNULL(A.KS_PERMIT_COPY_ORIGINAL_NAME, '') AS ks_permit_copy_original_name,
									IFNULL(A.KS_PERMIT_COPY_CHANGE_NAME, '') AS ks_permit_copy_change_name,
									IFNULL(A.CATALOG_PATH, '') AS catalog_path,
									IFNULL(A.CATALOG_ORIGINAL_NAME, '') AS catalog_original_name,
									IFNULL(A.CATALOG_CHANGE_NAME, '') AS catalog_change_name,
									IFNULL(A.BUSINESS_LICENSE_PATH, '') AS business_license_path,
									IFNULL(A.BUSINESS_LICENSE_ORIGINAL_NAME, '') AS business_license_original_name,
									IFNULL(A.BUSINESS_LICENSE_CHANGE_NAME, '') AS business_license_change_name,
									IFNULL(A.TAX_PAYMENT_CERTIFICATE_PATH, '') AS tax_payment_certificate_path,
									IFNULL(A.TAX_PAYMENT_CERTIFICATE_ORIGINAL_NAME, '') AS tax_payment_certificate_original_name,
									IFNULL(A.TAX_PAYMENT_CERTIFICATE_CHANGE_NAME, '') AS tax_payment_certificate_change_name,
									IFNULL(A.PERFORM_CERTIFICATE_PATH, '') AS perform_certificate_path,
									IFNULL(A.PERFORM_CERTIFICATE_ORIGINAL_NAME, '') AS perform_certificate_original_name,
									IFNULL(A.PERFORM_CERTIFICATE_CHANGE_NAME, '') AS perform_certificate_change_name,
									IFNULL(A.KFI_CERTIFICATE_PATH, '') AS kfi_certificate_path,
									IFNULL(A.KFI_CERTIFICATE_ORIGINAL_NAME, '') AS kfi_certificate_original_name,
									IFNULL(A.KFI_CERTIFICATE_CHANGE_NAME, '') AS kfi_certificate_change_name,
									IFNULL(A.FACTORY_CERTIFICATE_PATH, '') AS factory_certificate_path,
									IFNULL(A.FACTORY_CERTIFICATE_ORIGINAL_NAME, '') AS factory_certificate_original_name,
									IFNULL(A.FACTORY_CERTIFICATE_CHANGE_NAME, '') AS factory_certificate_change_name,
									IFNULL(A.TEST_RESULT_PATH, '') AS test_result_path,
									IFNULL(A.TEST_RESULT_ORIGINAL_NAME, '') AS test_result_original_name,
									IFNULL(A.TEST_RESULT_CHANGE_NAME, '') AS test_result_change_name,
									IFNULL(A.DELIVER_PERFORM_PATH, '') AS deliver_perform_path,
									IFNULL(A.DELIVER_PERFORM_ORIGINAL_NAME, '') AS deliver_perform_original_name,
									IFNULL(A.DELIVER_PERFORM_CHANGE_NAME, '') AS deliver_perform_change_name,
									IFNULL(A.SAMPLE_PATH, '') AS sample_path,
									IFNULL(A.SAMPLE_ORIGINAL_NAME, '') AS sample_original_name,
									IFNULL(A.SAMPLE_CHANGE_NAME, '') AS sample_change_name,
									IFNULL(A.USE_TYPE, '') AS use_type,
									IFNULL(A.STANDARD_NUM, '') AS standard_num
								FROM
									MATERIAL_MANAGE A
								WHERE
									1=1 """

INSERT_MATERIALMANAGE_INFO = """INSERT INTO MATERIAL_MANAGE(PRODUCE_CO, MATERIAL_NAME, APPROVAL_NUM, APPROVAL_DATE, FORMAL_NAME, KS_WHETHER, UPDATE_DATE, COLLECT_TYPE, STANDARD, NOTE) """

UPDATE_MATERIALMANAGE_INFO = """UPDATE MATERIAL_MANAGE SET """


class sqlProjectApproMaterManage:

    # 승인 자재 리스트를 조회 한다
    def sGetApproMaterList(self, params):
        commUtilServ = commUtilService()

        query = "SELECT * FROM ("
        query += SELECT_MATERIALMANAGE_INFO

        if commUtilServ.dataCheck(params["search_material_name"]) != False:
            query += (
                'AND A.MATERIAL_NAME LIKE "%' + params["search_material_name"] + '%" '
            )

        if commUtilServ.dataCheck(params["search_standard"]) != False:
            query += 'AND A.STANDARD = "' + params["search_standard"] + '" '

        if commUtilServ.dataCheck(params["search_produce_co"]) != False:
            query += 'AND A.PRODUCE_CO LIKE "%' + params["search_produce_co"] + '%" '

        if commUtilServ.dataCheck(params["search_approval_num"]) != False:
            query += (
                'AND A.APPROVAL_NUM LIKE "%' + params["search_approval_num"] + '%" '
            )

        if commUtilServ.dataCheck(params["search_start_approval_date"]) != False:
            query += (
                'AND A.APPROVAL_DATE >= "' + params["search_start_approval_date"] + '" '
            )

        if commUtilServ.dataCheck(params["search_end_approval_date"]) != False:
            query += (
                'AND A.APPROVAL_DATE <= "' + params["search_end_approval_date"] + '" '
            )

        if commUtilServ.dataCheck(params["search_formal_name"]) != False:
            query += 'AND A.FORMAL_NAME LIKE "%' + params["search_formal_name"] + '%" '

        if commUtilServ.dataCheck(params["search_use_type"]) != False:
            query += 'AND A.USE_TYPE = "' + params["search_use_type"] + '" '

        if params.get("search_unit") != None:
            if commUtilServ.dataCheck(params["search_unit"]) != False:
                query += 'AND A.UNIT = "' + params["search_unit"] + '" '

        query += ") B WHERE 1=1 "

        query += "ORDER BY " + params["sort_column"] + " " + params["sort_type"] + " "
        query += "LIMIT " + params["start_num"] + ", " + params["end_num"]

        return query

    # 승인 자재 리스트 개수를 조회 한다.
    def sGetApproMaterCnt(self, params):
        commUtilServ = commUtilService()

        query = "SELECT COUNT(*) AS cnt FROM ("
        query += SELECT_MATERIALMANAGE_INFO

        if commUtilServ.dataCheck(params["search_material_name"]) != False:
            query += (
                'AND A.MATERIAL_NAME LIKE "%' + params["search_material_name"] + '%" '
            )

        if commUtilServ.dataCheck(params["search_standard"]) != False:
            query += 'AND A.STANDARD = "' + params["search_standard"] + '" '

        if commUtilServ.dataCheck(params["search_produce_co"]) != False:
            query += 'AND A.PRODUCE_CO LIKE "%' + params["search_produce_co"] + '%" '

        if commUtilServ.dataCheck(params["search_approval_num"]) != False:
            query += (
                'AND A.APPROVAL_NUM LIKE "%' + params["search_approval_num"] + '%" '
            )

        if commUtilServ.dataCheck(params["search_start_approval_date"]) != False:
            query += (
                'AND A.APPROVAL_DATE >= "' + params["search_start_approval_date"] + '" '
            )

        if commUtilServ.dataCheck(params["search_end_approval_date"]) != False:
            query += (
                'AND A.APPROVAL_DATE <= "' + params["search_end_approval_date"] + '" '
            )

        if commUtilServ.dataCheck(params["search_formal_name"]) != False:
            query += 'AND A.FORMAL_NAME LIKE "%' + params["search_formal_name"] + '%" '

        if commUtilServ.dataCheck(params["search_use_type"]) != False:
            query += 'AND A.USE_TYPE = "' + params["search_use_type"] + '" '

        query += ") B WHERE 1=1 "

        return query

    # 승인 자재를 상세 조회 한다.
    def sGetDetailApproMater(self, materialNo):

        query = SELECT_MATERIALMANAGE_INFO

        query += 'AND A.MATERIAL_NUM = "' + materialNo + '" '

        return query

    # 수동 입력되는 자재를 검색 한다.
    def sGetManualInputMaterialInfo(self, searchInfo):

        query = SELECT_MATERIALMANAGE_INFO

        if len(searchInfo) > 0:
            for search in searchInfo:
                if search["type"] == "string":
                    query += (
                        "AND A." + search["column"] + ' = "' + search["data"] + '" '
                    )
                elif search["type"] == "int":
                    query += (
                        "AND A." + search["column"] + " = " + str(search["data"]) + " "
                    )

        return query

    # 수동 입력되는 자재 정보를 저장 한다.
    def iPutManualInputMaterialInfo(self, materialInfo):

        query = INSERT_MATERIALMANAGE_INFO

        query += "VALUES( "
        query += '"' + materialInfo["produce_co"] + '", '
        query += '"' + materialInfo["material_name"] + '", '
        query += '"' + materialInfo["approval_num"] + '", '
        query += '"' + materialInfo["approval_date"] + '", '
        query += '"' + materialInfo["formal_name"] + '", '
        query += '"' + materialInfo["ks_whether"] + '", '
        query += '"' + materialInfo["update_date"] + '", '
        query += '"M", '
        query += '"' + materialInfo["standard"] + '", '
        query += '"' + materialInfo["note"] + '"'

        return query

    # 수동 입력되는 자재 정보를 업데이트 한다.
    def uModifyManualInputMaterialInfo(self, materialInfo):

        query = UPDATE_MATERIALMANAGE_INFO

        query += 'MATERIAL_NAME = "' + materialInfo["material_name"] + '", '
        query += 'STANDARD = "' + materialInfo["standard"] + '", '
        query += 'FORMAL_NAME = "' + materialInfo["formal_name"] + '", '
        query += 'PRODUCE_CO = "' + materialInfo["produce_co"] + '", '
        query += 'APPROVAL_NUM = "' + materialInfo["approval_num"] + '", '
        query += 'KS_WHETHER = "' + materialInfo["ks_whether"] + '", '
        query += 'APPROVAL_DATE = "' + materialInfo["approval_date"] + '", '
        query += 'NOTE = "' + materialInfo["note"] + '", '
        query += (
            'BUSINESS_LICENSE_PATH = "' + materialInfo["business_license_path"] + '", '
        )
        query += (
            'BUSINESS_LICENSE_ORIGINAL_NAME = "'
            + materialInfo["business_license_original_name"]
            + '", '
        )
        query += (
            'BUSINESS_LICENSE_CHANGE_NAME = "'
            + materialInfo["business_license_change_name"]
            + '", '
        )
        query += (
            'PERFORM_CERTIFICATE_PATH = "'
            + materialInfo["perform_certificate_path"]
            + '", '
        )
        query += (
            'PERFORM_CERTIFICATE_ORIGINAL_NAME = "'
            + materialInfo["perform_certificate_original_name"]
            + '", '
        )
        query += (
            'PERFORM_CERTIFICATE_CHANGE_NAME = "'
            + materialInfo["perform_certificate_change_name"]
            + '", '
        )
        query += (
            'TAX_PAYMENT_CERTIFICATE_PATH = "'
            + materialInfo["tax_payment_certificate_path"]
            + '", '
        )
        query += (
            'TAX_PAYMENT_CERTIFICATE_ORIGINAL_NAME = "'
            + materialInfo["tax_payment_certificate_original_name"]
            + '", '
        )
        query += (
            'TAX_PAYMENT_CERTIFICATE_CHANGE_NAME = "'
            + materialInfo["tax_payment_certificate_change_name"]
            + '", '
        )
        query += (
            'KFI_CERTIFICATE_PATH = "' + materialInfo["kfi_certificate_path"] + '", '
        )
        query += (
            'KFI_CERTIFICATE_ORIGINAL_NAME = "'
            + materialInfo["kfi_certificate_original_name"]
            + '", '
        )
        query += (
            'KFI_CERTIFICATE_CHANGE_NAME = "'
            + materialInfo["kfi_certificate_change_name"]
            + '", '
        )
        query += 'KS_PERMIT_COPY_PATH = "' + materialInfo["ks_permit_copy_path"] + '", '
        query += (
            'KS_PERMIT_COPY_ORIGINAL_NAME = "'
            + materialInfo["ks_permit_copy_original_name"]
            + '", '
        )
        query += (
            'KS_PERMIT_COPY_CHANGE_NAME = "'
            + materialInfo["ks_permit_copy_change_name"]
            + '", '
        )
        query += (
            'FACTORY_CERTIFICATE_PATH = "'
            + materialInfo["factory_certificate_path"]
            + '", '
        )
        query += (
            'FACTORY_CERTIFICATE_ORIGINAL_NAME = "'
            + materialInfo["factory_certificate_original_name"]
            + '", '
        )
        query += (
            'FACTORY_CERTIFICATE_CHANGE_NAME = "'
            + materialInfo["factory_certificate_change_name"]
            + '", '
        )
        query += 'CATALOG_PATH = "' + materialInfo["catalog_path"] + '", '
        query += (
            'CATALOG_ORIGINAL_NAME = "' + materialInfo["catalog_original_name"] + '", '
        )
        query += 'CATALOG_CHANGE_NAME = "' + materialInfo["catalog_change_name"] + '", '
        query += 'TEST_RESULT_PATH = "' + materialInfo["test_result_path"] + '", '
        query += (
            'TEST_RESULT_ORIGINAL_NAME = "'
            + materialInfo["test_result_original_name"]
            + '", '
        )
        query += (
            'TEST_RESULT_CHANGE_NAME = "'
            + materialInfo["test_result_change_name"]
            + '", '
        )
        query += (
            'DELIVER_PERFORM_PATH = "' + materialInfo["deliver_perform_path"] + '", '
        )
        query += (
            'DELIVER_PERFORM_ORIGINAL_NAME = "'
            + materialInfo["deliver_perform_original_name"]
            + '", '
        )
        query += (
            'DELIVER_PERFORM_CHANGE_NAME = "'
            + materialInfo["deliver_perform_change_name"]
            + '", '
        )
        query += 'SAMPLE_PATH = "' + materialInfo["sample_path"] + '", '
        query += (
            'SAMPLE_ORIGINAL_NAME = "' + materialInfo["sample_original_name"] + '", '
        )
        query += 'SAMPLE_CHANGE_NAME = "' + materialInfo["sample_change_name"] + '" '

        query += "WHERE MATERIAL_NUM = " + str(materialInfo["material_num"]) + " "

        return query
