# -*- coding: utf-8 -*-
import sys
import time
from flask import json, current_app
from sqlalchemy import func, text
from herovii import db
from herovii.libs.error_code import NotFound, FileUploadFailed
from herovii.libs.helper import get_oss_file_url
from herovii.libs.oss import OssAPI
from herovii.models.InformationFlow.information_flow_banner import InformationFlowBanner
from herovii.models.org.teaching_course_enroll import TeachingCourseEnroll
from herovii.models.overseas.country import Country
from herovii.models.overseas.organization_to_university import OrganizationToUniversity
from herovii.models.overseas.overseas_plan import OverseasPlan
from herovii.models.overseas.university import University
from herovii.models.overseas.university_major import UniversityMajor
from herovii.models.overseas.university_photos import UniversityPhotos
from herovii.service.file import FilePiper

__author__ = 'yangchujie'


def get_overseas_study_banner_service(page, per_page):
    banner_count = db.session.query(InformationFlowBanner).filter(InformationFlowBanner.status == 1,
                                                                  InformationFlowBanner.show_pos == 3).count()
    data_list = []
    start = (page - 1) * per_page
    stop = start + per_page
    banner_list = db.session.query(InformationFlowBanner) \
        .filter(InformationFlowBanner.status == 1,
                InformationFlowBanner.show_pos == 3) \
        .slice(start, stop) \
        .all()
    if banner_list:
        for banner in banner_list:
            jump_type = banner.jump_type
            banner_object = {
                'id': banner.id,
                'pic_url': banner.pic_url,
                'jump_type': jump_type,
                'url': banner.url
            }
            if jump_type == 2:
                post_id = banner.url
                banner_object['url'] = 'hisihi://post/detailinfo?id=' + post_id
            elif jump_type == 3:
                course_id = banner.url
                banner_object['url'] = 'hisihi://course/detailinfo?id=' + course_id
            elif jump_type == 4:
                org_id = banner.url
                banner_object['url'] = 'hisihi://organization/detailinfo?id=' + org_id
            elif jump_type == 5:
                university_id = banner.url
                banner_object['url'] = 'hisihi://university/detailinfo?id=' + university_id
            data_list.append(banner_object)
    return banner_count, data_list


def get_overseas_study_hot_country_service(page, per_page):
    country_count = db.session.query(Country).filter(Country.status == 1,
                                                     Country.is_hot == 1).count()
    data_list = []
    start = (page - 1) * per_page
    stop = start + per_page
    country_list = db.session.query(Country.id, Country.name, Country.logo_url) \
        .filter(Country.status == 1,
                Country.is_hot == 1) \
        .order_by(Country.create_time.desc()) \
        .slice(start, stop) \
        .all()
    for country in country_list:
        data = {
            'id': country.id,
            'name': country.name,
            'logo_url': country.logo_url
        }
        data_list.append(data)
    return country_count, data_list


def get_overseas_study_country_service(page, per_page):
    country_count = db.session.query(Country).filter(Country.status == 1).count()
    data_list = []
    start = (page - 1) * per_page
    stop = start + per_page
    country_list = db.session.query(Country.id, Country.name, Country.logo_url) \
        .filter(Country.status == 1) \
        .order_by(Country.create_time.desc()) \
        .slice(start, stop) \
        .all()
    for country in country_list:
        university_count = db.session.query(University).filter(University.status == 1,
                                                               University.country_id == country.id).count()
        university_list = db.session.query(University.id, University.name, University.logo_url) \
            .filter(University.status == 1,
                    University.country_id == country.id) \
            .order_by(University.create_time.desc()) \
            .slice(start, stop) \
            .all()
        enroll_total_count = 0
        for university in university_list:
            teaching_course_list = db.session.query(OrganizationToUniversity) \
                .filter(OrganizationToUniversity.status == 1,
                        OrganizationToUniversity.teaching_course_id != 0,
                        OrganizationToUniversity.university_id == university.id) \
                .all()
            if len(teaching_course_list) == 0:
                enroll_total_count = 0
            else:
                teaching_course_id_list = []
                for teaching_course in teaching_course_list:
                    teaching_course_id_list.append(str(teaching_course.teaching_course_id))
                enroll_total_count = db.session.query(TeachingCourseEnroll) \
                    .filter(TeachingCourseEnroll.status == 1,
                            func.find_in_set(TeachingCourseEnroll.course_id, ','.join(teaching_course_id_list))) \
                    .count()
        data = {
            'id': country.id,
            'name': country.name,
            'logo_url': country.logo_url,
            'university_total_count': university_count,
            'enroll_total_count': enroll_total_count
        }
        data_list.append(data)
    return country_count, data_list


def get_overseas_study_hot_university_service(page, per_page):
    university_count = db.session.query(University).filter(University.status == 1,
                                                           University.is_hot == 1).count()
    data_list = []
    start = (page - 1) * per_page
    stop = start + per_page
    university_list = db.session.query(University.id, University.name, University.logo_url) \
        .filter(University.status == 1,
                University.is_hot == 1) \
        .order_by(University.create_time.desc()) \
        .slice(start, stop) \
        .all()
    for university in university_list:
        data = {
            'id': university.id,
            'name': university.name,
            'logo_url': university.logo_url
        }
        data_list.append(data)
    return university_count, data_list


def get_overseas_study_university_info_service(uid):
    university = University.query.get(uid)
    if not university:
        raise NotFound(error_code=5008, error='大学信息不存在')
    graduate_majors_array = university.graduate_majors.split("#")
    undergraduate_majors_array = university.undergraduate_majors.split("#")
    graduate_major_text = []
    undergraduate_major_text = []
    for graduate_major_id in graduate_majors_array:
        major_info = UniversityMajor.query.get(graduate_major_id)
        if major_info:
            graduate_major_text.append(major_info.name)
    for undergraduate_major_id in undergraduate_majors_array:
        major_info = UniversityMajor.query.get(undergraduate_major_id)
        if major_info:
            undergraduate_major_text.append(major_info.name)
    server_host_name = current_app.config['SERVER_HOST_NAME']
    web_url = server_host_name + "/api.php?s=/university/showuniversitymainpage/university_id/" + str(uid)
    share_url = web_url
    return {
        'name': university.name,
        'website': university.website,
        'logo_url': university.logo_url,
        'undergraduate_major': undergraduate_major_text,
        'graduate_major': graduate_major_text,
        'introduction': university.introduction,
        'sia_recommend_level': university.sia_recommend_level,
        'sia_student_enrollment_rate': university.sia_student_enrollment_rate,
        'difficulty_of_application': university.difficulty_of_application,
        'tuition_fees': university.tuition_fees,
        'toefl': university.toefl,
        'ielts': university.ielts,
        'proportion_of_undergraduates': university.proportion_of_undergraduates,
        'scholarship': university.scholarship,
        'deadline_for_applications': university.deadline_for_applications,
        'application_requirements': university.application_requirements,
        'school_environment': university.school_environment,
        'web_url': web_url,
        'share_url': share_url
    }


def get_overseas_study_university_list_by_country_id_service(cid, page, per_page):
    university_count = db.session.query(University).filter(University.status == 1,
                                                           University.country_id == cid).count()
    data_list = []
    start = (page - 1) * per_page
    stop = start + per_page
    university_list = db.session.query(University.id, University.name, University.logo_url) \
        .filter(University.status == 1,
                University.country_id == cid) \
        .order_by(University.create_time.desc()) \
        .slice(start, stop) \
        .all()
    for university in university_list:
        organization_total_count = db.session.query(OrganizationToUniversity).filter(
            OrganizationToUniversity.status == 1,
            OrganizationToUniversity.teaching_course_id == 0,
            OrganizationToUniversity.university_id == university.id).count()
        teaching_course_list = db.session.query(OrganizationToUniversity) \
            .filter(OrganizationToUniversity.status == 1,
                    OrganizationToUniversity.teaching_course_id != 0,
                    OrganizationToUniversity.university_id == university.id) \
            .all()
        if len(teaching_course_list) == 0:
            enroll_total_count = 0
        else:
            teaching_course_id_list = []
            for teaching_course in teaching_course_list:
                teaching_course_id_list.append(str(teaching_course.teaching_course_id))
            enroll_total_count = db.session.query(TeachingCourseEnroll) \
                .filter(TeachingCourseEnroll.status == 1,
                        func.find_in_set(TeachingCourseEnroll.course_id, ','.join(teaching_course_id_list))) \
                .count()
        data = {
            'id': university.id,
            'name': university.name,
            'logo_url': university.logo_url,
            'organization_total_count': organization_total_count,
            'enroll_total_count': enroll_total_count
        }
        data_list.append(data)
    return university_count, data_list


def get_overseas_study_university_photos_service(uid, page, per_page):
    photos_count = db.session.query(UniversityPhotos).filter(UniversityPhotos.status == 1,
                                                             UniversityPhotos.university_id == uid).count()
    data_list = {}
    start = (page - 1) * per_page
    stop = start + per_page
    photo_list = db.session.query(UniversityPhotos.id, UniversityPhotos.descript, UniversityPhotos.pic_url) \
        .filter(UniversityPhotos.status == 1,
                UniversityPhotos.university_id == uid) \
        .order_by(UniversityPhotos.create_time.desc()) \
        .slice(start, stop) \
        .all()
    if photo_list:
        p_list = []
        for photo in photo_list:
            photo_obj = {
                "id": photo.id,
                "descript": photo.descript,
                "pic_url": photo.pic_url
            }
            p_list.append(photo_obj)
        data_list['count'] = photos_count
        data_list['list'] = p_list
    else:
        data_list['count'] = 0
        data_list['list'] = None
    return data_list


def get_overseas_study_university_majors_service(uid):
    majors = db.session.query(University.undergraduate_majors, University.graduate_majors) \
        .filter(University.status == 1, University.id == uid).first()
    major_array = []
    undergraduate_majors = majors.undergraduate_majors.split('#')
    graduate_majors = majors.graduate_majors.split('#')
    if undergraduate_majors:
        major_array.extend(undergraduate_majors)
    if graduate_majors:
        major_array.extend(graduate_majors)
    data_list = {}
    major_list = db.session.query(UniversityMajor.name, UniversityMajor.id) \
        .filter(UniversityMajor.status == 1,
                UniversityMajor.id.in_(major_array)) \
        .all()
    if major_list:
        p_list = []
        for major in major_list:
            major_obj = {
                "id": major.id,
                "name": major.name,
            }
            p_list.append(major_obj)
        data_list['count'] = len(p_list)
        data_list['list'] = p_list
    else:
        data_list['count'] = 0
        data_list['list'] = None
    return data_list


def get_overseas_study_university_list_service():
    data_list = []
    university_list = db.session.query(University.id, University.name) \
        .filter(University.status == 1) \
        .order_by(text("CONVERT( name USING gbk ) COLLATE gbk_chinese_ci ASC")) \
        .all()
    for university in university_list:
        data = {
            'id': university.id,
            'name': university.name,
        }
        data_list.append(data)
    return data_list


def put_overseas_article_service(oid, text, url):
    plan = OverseasPlan()
    plan.organization_id = oid
    plan.html_content = text
    plan.url = url
    plan.create_time = int(time.time())
    plan.status = 1
    with db.auto_commit():
        db.session.add(plan)
    return plan


def get_org_overseas_plan_list_service(oid):
    data_list = []
    plan_list = db.session.query(OverseasPlan.id, OverseasPlan.url) \
        .filter(OverseasPlan.organization_id == oid, OverseasPlan.status == 1) \
        .order_by(OverseasPlan.create_time.desc()) \
        .all()
    for plan in plan_list:
        data = {
            'id': plan.id,
            'url': plan.url,
        }
        data_list.append(data)
    return data_list


def get_org_overseas_plan_detail_service(pid):
    detail = db.session.query(OverseasPlan).filter(OverseasPlan.id == pid).first()
    return detail


