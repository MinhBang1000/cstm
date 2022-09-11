def get_error(name):
    return {
        "detail": name
    }

EMAIL_NOT_SENT = "Something went wrong! Can't send email"
EMAIL_EXSITS = "This email have already exists! Please choose another"
EMAIL_NOT_EXISTS = "Haven't exists user follow this email! Please check them again"
PASSWORD_CONFIRM = "Both password and confirm was not same! Please check it again"
PIN_INCORRECT = "PIN was not correct!"
CHANGE_OWNER = "You can't change owner of this storage!"
NOT_FOUND_OPERATE = "This operation is not exsits!"
NOT_ANONYMUS = "This user can not be invited to your storage!"
ROLE_NOT_EXISTS = "This role doesn't exists!"
ONE_MAN_TO_ONE_ROLE = "This person have already been invited!"
NOT_FOUND_STORAGE = "Can't found any storage which you have follow this id!"
NOT_FOUND_INVITATION = "Can't found any invitation which you define!"
NOT_YOUR_INVITATION = "This invitation is not your!"
NOT_YOUR_PERMIT = "This invitation must be decided by owner!"
CAN_ACCESS_STORAGE = "You haven't role for this storage!"
DATA_TYPE_INVALID = "This data type is invalid!"
REQUEST_NOT_HAVE_STORAGE_ID = "Your request has not storage_id field!"
DAY_TIME = "This monitor time is invalid with day's time!"
TEMPERATURE_VALID = "Min of temperature must be set smaller than max of temperature!"
CHANGE_STORAGE = "Can not change storage of area!"
CHANGE_EMPLOYEE = "Can not change creater of area!"
NOT_FOUND_PROVINCE = "Can't found any province which you have follow this id!"
PROVINCE_EXISTS = "This province's name has already exists!"
COMPANY_CHANGE_OWNER = "You can't change owner of any companies!"