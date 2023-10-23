# _*_coding: utf-8 -*-
import os
import sys
import copy

from allscapeAPIMain import db
from allscapeAPIMain import procName
from allscapeAPIMain import materialHome
from allscapeAPIMain import materialFile


from common.logManage import logManage

from projectApproMaterManage.sqlProjectApproMaterManage import (
    sqlProjectApproMaterManage,
)
from common.commonService import commonService


logs = logManage()  # 사용자 관리 API 로그를 남기기 위한 객체 할당


class servProjectApproMaterManage:

    # 승인 자재 리스트를 조회 한다.
    def getApproMaterList(self, params):
        dbms = copy.copy(db)
        sProjApproMaterMana = sqlProjectApproMaterManage()

        query = sProjApproMaterMana.sGetApproMaterList(params)

        logs.debug(
            procName,
            os.path.basename(__file__),
            sys._getframe(0).f_code.co_name,
            "sGetApproMaterList Query : " + query,
        )
        # 쿼리 실행
        resCd, msg, resData = dbms.query(query)

        return resCd, msg, resData

    # 승인 자재 개수를 조회 한다.
    def getApproMaterCnt(self, params):
        dbms = copy.copy(db)
        sProjApproMaterMana = sqlProjectApproMaterManage()

        query = sProjApproMaterMana.sGetApproMaterCnt(params)

        logs.debug(
            procName,
            os.path.basename(__file__),
            sys._getframe(0).f_code.co_name,
            "sGetApproMaterCnt Query : " + query,
        )
        # 쿼리 실행
        resCd, msg, resData = dbms.queryForObject(query)

        return resCd, msg, resData

    # 승인 자재를 상세 조회 한다.
    def getDetailApproMater(self, materialNo):
        dbms = copy.copy(db)
        sProjApproMaterMana = sqlProjectApproMaterManage()

        query = sProjApproMaterMana.sGetDetailApproMater(materialNo)

        logs.debug(
            procName,
            os.path.basename(__file__),
            sys._getframe(0).f_code.co_name,
            "sGetDetailApproMater Query : " + query,
        )
        # 쿼리 실행
        resCd, msg, resData = dbms.queryForObject(query)

        return resCd, msg, resData

    # 수동 입력 되는 자재를 검색 한다.
    def getManualInputMaterialInfo(self, searchInfo):
        dbms = copy.copy(db)
        sProjApproMaterMana = sqlProjectApproMaterManage()

        query = sProjApproMaterMana.sGetManualInputMaterialInfo(searchInfo)

        logs.debug(
            procName,
            os.path.basename(__file__),
            sys._getframe(0).f_code.co_name,
            "sGetManualInputMaterialInfo Query : " + query,
        )
        # 쿼리 실행
        resCd, msg, resData = dbms.queryForObject(query)

        return resCd, msg, resData

    # 수동 입력 자재 정보를 저장 한다.
    def putManualInputMaterialInfo(self, materialInfo):
        dbms = copy.copy(db)
        sProjApproMaterMana = sqlProjectApproMaterManage()

        query = sProjApproMaterMana.iPutManualInputMaterialInfo(materialInfo)

        logs.debug(
            procName,
            os.path.basename(__file__),
            sys._getframe(0).f_code.co_name,
            "iPutManualInputMaterialInfo Query : " + query,
        )
        # 쿼리 실행
        resCd, msg, resData = dbms.execute(query)

        return resCd, msg, resData

    # 수동 입력 자재 정보를 업데이트 한다.
    def modifyManualInputMaterialInfo(self, materialInfo):
        dbms = copy.copy(db)
        sProjApproMaterMana = sqlProjectApproMaterManage()

        query = sProjApproMaterMana.uModifyManualInputMaterialInfo(materialInfo)

        logs.debug(
            procName,
            os.path.basename(__file__),
            sys._getframe(0).f_code.co_name,
            "uModifyManualInputMaterialInfo Query : " + query,
        )
        # 쿼리 실행
        resCd, msg, resData = dbms.execute(query)

        return resCd, msg, resData

    # 자재 파일 정보를 관리 한다.
    def materialFileManage(self, materialInfo, resultMaterialInfo, req, index):
        commServ = commonService()

        resultMaterialInfo["constructor_comments"] = materialInfo[
            "constructor_comments"
        ]
        resultMaterialInfo["remarks"] = materialInfo["remarks"]

        if materialInfo["business_license_type"] == "Y":
            path, origName, changeName = commServ.createFilePathAndName(
                materialHome,
                materialInfo["business_license_type"],
                materialFile.replace("{materialNum}", str(materialInfo["material_num"]))
                + "businessLicense/",
                materialInfo,
                "business_license_name_new",
            )

            resultMaterialInfo["business_license_path"] = path
            resultMaterialInfo["business_license_original_name"] = origName
            resultMaterialInfo["business_license_change_name"] = changeName

            # resultMaterialInfo['business_license_path'],
            # resultMaterialInfo['business_license_original_name'],
            # resultMaterialInfo['business_license_change_name'] = commServ.createFilePathAndName(materialHome,
            # 		materialInfo['business_license_type'],
            # 		materialFile.replace('{materialNum}', str(materialInfo['material_num'])) + 'businessLicense/',
            # 		materialInfo,
            # 		'business_license_name_new')

            commServ.createDir(resultMaterialInfo["business_license_path"])
            commServ.saveFile(
                req.files["f_" + str(index) + "_business_license"],
                resultMaterialInfo["business_license_path"],
                resultMaterialInfo["business_license_change_name"],
            )

        if materialInfo["perform_certificate_type"] == "Y":
            path, origName, changeName = commServ.createFilePathAndName(
                materialHome,
                materialInfo["perform_certificate_type"],
                materialFile.replace("{materialNum}", str(materialInfo["material_num"]))
                + "performCertificate/",
                materialInfo,
                "perform_certificate_name_new",
            )

            resultMaterialInfo["perform_certificate_path"] = path
            resultMaterialInfo["perform_certificate_original_name"] = origName
            resultMaterialInfo["perform_certificate_change_name"] = changeName

            # resultMaterialInfo['perform_certificate_path'],
            # resultMaterialInfo['perform_certificate_original_name'],
            # resultMaterialInfo['perform_certificate_change_name'] = commServ.createFilePathAndName(materialHome,
            # 		materialInfo['perform_certificate_type'],
            # 		materialFile.replace('{materialNum}', str(materialInfo['material_num'])) + 'performCertificate/',
            # 		materialInfo,
            # 		'perform_certificate_name_new')

            commServ.createDir(resultMaterialInfo["perform_certificate_path"])
            commServ.saveFile(
                req.files["f_" + str(index) + "_perform_certificate"],
                resultMaterialInfo["perform_certificate_path"],
                resultMaterialInfo["perform_certificate_change_name"],
            )

        if materialInfo["ks_permit_copy_type"] == "Y":
            path, origName, changeName = commServ.createFilePathAndName(
                materialHome,
                materialInfo["ks_permit_copy_type"],
                materialFile.replace("{materialNum}", str(materialInfo["material_num"]))
                + "ksPermitCopy/",
                materialInfo,
                "ks_permit_copy_name_new",
            )

            resultMaterialInfo["ks_permit_copy_path"] = path
            resultMaterialInfo["ks_permit_copy_original_name"] = origName
            resultMaterialInfo["ks_permit_copy_change_name"] = changeName

            # resultMaterialInfo['ks_permit_copy_path'],
            # resultMaterialInfo['ks_permit_copy_original_name'],
            # resultMaterialInfo['ks_permit_copy_change_name'] = commServ.createFilePathAndName(materialHome,
            # 		materialInfo['ks_permit_copy_type'],
            # 		materialFile.replace('{materialNum}', str(materialInfo['material_num'])) + 'ksPermitCopy/',
            # 		materialInfo,
            # 		'ks_permit_copy_name_new')

            commServ.createDir(resultMaterialInfo["ks_permit_copy_path"])
            commServ.saveFile(
                req.files["f_" + str(index) + "_ks_permit_copy"],
                resultMaterialInfo["ks_permit_copy_path"],
                resultMaterialInfo["ks_permit_copy_change_name"],
            )

        if materialInfo["tax_payment_certificate_type"] == "Y":

            path, origName, changeName = commServ.createFilePathAndName(
                materialHome,
                materialInfo["tax_payment_certificate_type"],
                materialFile.replace("{materialNum}", str(materialInfo["material_num"]))
                + "taxPaymentCertificate/",
                materialInfo,
                "tax_payment_certificate_name_new",
            )

            resultMaterialInfo["tax_payment_certificate_path"] = path
            resultMaterialInfo["tax_payment_certificate_original_name"] = origName
            resultMaterialInfo["tax_payment_certificate_change_name"] = changeName

            # resultMaterialInfo['tax_payment_certificate_path'],
            # resultMaterialInfo['tax_payment_certificate_original_name'],
            # resultMaterialInfo['tax_payment_certificate_change_name'] = commServ.createFilePathAndName(materialHome,
            # 		materialInfo['tax_payment_certificate_type'],
            # 		materialFile.replace('{materialNum}', str(materialInfo['material_num'])) + 'taxPaymentCertificate/',
            # 		materialInfo,
            # 		'tax_payment_certificate_name_new')

            commServ.createDir(resultMaterialInfo["tax_payment_certificate_path"])
            commServ.saveFile(
                req.files["f_" + str(index) + "_tax_payment_certificate"],
                resultMaterialInfo["tax_payment_certificate_path"],
                resultMaterialInfo["tax_payment_certificate_change_name"],
            )

        if materialInfo["kfi_certificate_type"] == "Y":
            path, origName, changeName = commServ.createFilePathAndName(
                materialHome,
                materialInfo["kfi_certificate_type"],
                materialFile.replace("{materialNum}", str(materialInfo["material_num"]))
                + "kfiCertificate/",
                materialInfo,
                "kfi_certificate_name_new",
            )

            resultMaterialInfo["kfi_certificate_path"] = path
            resultMaterialInfo["kfi_certificate_original_name"] = origName
            resultMaterialInfo["kfi_certificate_change_name"] = changeName

            # resultMaterialInfo['kfi_certificate_path'],
            # resultMaterialInfo['kfi_certificate_original_name'],
            # resultMaterialInfo['kfi_certificate_change_name'] = commServ.createFilePathAndName(materialHome,
            # 		materialInfo['kfi_certificate_type'],
            # 		materialFile.replace('{materialNum}', str(materialInfo['material_num'])) + 'kfiCertificate/',
            # 		materialInfo,
            # 		'kfi_certificate_name_new')

            commServ.createDir(resultMaterialInfo["kfi_certificate_path"])
            commServ.saveFile(
                req.files["f_" + str(index) + "_kfi_certificate"],
                resultMaterialInfo["kfi_certificate_path"],
                resultMaterialInfo["kfi_certificate_change_name"],
            )

        if materialInfo["factory_certificate_type"] == "Y":
            path, origName, changeName = commServ.createFilePathAndName(
                materialHome,
                materialInfo["factory_certificate_type"],
                materialFile.replace("{materialNum}", str(materialInfo["material_num"]))
                + "factoryCertificate/",
                materialInfo,
                "factory_certificate_name_new",
            )

            resultMaterialInfo["factory_certificate_path"] = path
            resultMaterialInfo["factory_certificate_original_name"] = origName
            resultMaterialInfo["factory_certificate_change_name"] = changeName

            # resultMaterialInfo['factory_certificate_path'],
            # resultMaterialInfo['factory_certificate_original_name'],
            # resultMaterialInfo['factory_certificate_change_name'] = commServ.createFilePathAndName(materialHome,
            # 		materialInfo['factory_certificate_type'],
            # 		materialFile.replace('{materialNum}', str(materialInfo['material_num'])) + 'factoryCertificate/',
            # 		materialInfo,
            # 		'factory_certificate_name_new')

            commServ.createDir(resultMaterialInfo["factory_certificate_path"])
            commServ.saveFile(
                req.files["f_" + str(index) + "_factory_certificate"],
                resultMaterialInfo["factory_certificate_path"],
                resultMaterialInfo["factory_certificate_change_name"],
            )

        if materialInfo["catalog_type"] == "Y":
            path, origName, changeName = commServ.createFilePathAndName(
                materialHome,
                materialInfo["catalog_type"],
                materialFile.replace("{materialNum}", str(materialInfo["material_num"]))
                + "catalog/",
                materialInfo,
                "catalog_name_new",
            )

            resultMaterialInfo["catalog_path"] = path
            resultMaterialInfo["catalog_original_name"] = origName
            resultMaterialInfo["catalog_change_name"] = changeName

            # resultMaterialInfo['catalog_path'],
            # resultMaterialInfo['catalog_original_name'],
            # resultMaterialInfo['catalog_change_name'] = commServ.createFilePathAndName(materialHome,
            # 		materialInfo['catalog_type'],
            # 		materialFile.replace('{materialNum}', str(materialInfo['material_num'])) + 'catalog/',
            # 		materialInfo,
            # 		'catalog_name_new')

            commServ.createDir(resultMaterialInfo["catalog_path"])
            commServ.saveFile(
                req.files["f_" + str(index) + "_catalog"],
                resultMaterialInfo["catalog_path"],
                resultMaterialInfo["catalog_change_name"],
            )

        if materialInfo["test_result_type"] == "Y":
            path, origName, changeName = commServ.createFilePathAndName(
                materialHome,
                materialInfo["test_result_type"],
                materialFile.replace("{materialNum}", str(materialInfo["material_num"]))
                + "testResult/",
                materialInfo,
                "test_result_name_new",
            )

            resultMaterialInfo["test_result_path"] = path
            resultMaterialInfo["test_result_original_name"] = origName
            resultMaterialInfo["test_result_change_name"] = changeName

            # resultMaterialInfo['test_result_path'],
            # resultMaterialInfo['test_result_original_name'],
            # resultMaterialInfo['test_result_change_name'] = commServ.createFilePathAndName(materialHome,
            # 		materialInfo['test_result_type'],
            # 		materialFile.replace('{materialNum}', str(materialInfo['material_num'])) + 'testResult/',
            # 		materialInfo,
            # 		'test_result_name_new')

            commServ.createDir(resultMaterialInfo["test_result_path"])
            commServ.saveFile(
                req.files["f_" + str(index) + "_test_result"],
                resultMaterialInfo["test_result_path"],
                resultMaterialInfo["test_result_change_name"],
            )

        if materialInfo["deliver_perform_type"] == "Y":
            path, origName, changeName = commServ.createFilePathAndName(
                materialHome,
                materialInfo["deliver_perform_type"],
                materialFile.replace("{materialNum}", str(materialInfo["material_num"]))
                + "deliverPerform/",
                materialInfo,
                "deliver_perform_name_new",
            )

            resultMaterialInfo["deliver_perform_path"] = path
            resultMaterialInfo["deliver_perform_original_name"] = origName
            resultMaterialInfo["deliver_perform_change_name"] = changeName

            # resultMaterialInfo['deliver_perform_path'],
            # resultMaterialInfo['deliver_perform_original_name'],
            # resultMaterialInfo['deliver_perform_change_name'] = commServ.createFilePathAndName(materialHome,
            # 		materialInfo['deliver_perform_type'],
            # 		materialFile.replace('{materialNum}', str(materialInfo['material_num'])) + 'deliverPerform/',
            # 		materialInfo,
            # 		'deliver_perform_name_new')

            commServ.createDir(resultMaterialInfo["deliver_perform_path"])
            commServ.saveFile(
                req.files["f_" + str(index) + "_deliver_perform"],
                resultMaterialInfo["deliver_perform_path"],
                resultMaterialInfo["deliver_perform_change_name"],
            )

        if materialInfo["sample_type"] == "Y":
            path, origName, changeName = commServ.createFilePathAndName(
                materialHome,
                materialInfo["sample_type"],
                materialFile.replace("{materialNum}", str(materialInfo["material_num"]))
                + "sample/",
                materialInfo,
                "sample_name_new",
            )

            resultMaterialInfo["sample_path"] = path
            resultMaterialInfo["sample_original_name"] = origName
            resultMaterialInfo["sample_change_name"] = changeName

            # resultMaterialInfo['sample_path'],
            # resultMaterialInfo['sample_original_name'],
            # resultMaterialInfo['sample_change_name'] = commServ.createFilePathAndName(materialHome,
            # 		materialInfo['sample_type'],
            # 		materialFile.replace('{materialNum}', str(materialInfo['material_num'])) + 'sample/',
            # 		materialInfo,
            # 		'sample_name_new')

            commServ.createDir(resultMaterialInfo["sample_path"])
            commServ.saveFile(
                req.files["f_" + str(index) + "_sample"],
                resultMaterialInfo["sample_path"],
                resultMaterialInfo["sample_change_name"],
            )

        return resultMaterialInfo
