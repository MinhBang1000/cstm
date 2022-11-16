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
CAN_NOT_PERFORM = "You can't perform this action, please do it again!"
ROLE_NOT_EXISTS = "This role doesn't exists!"
ONE_MAN_TO_ONE_ROLE = "This person have already been invited!"
NOT_FOUND_STORAGE = "Can't found any storage which you have follow this id!"
NOT_FOUND_INVITATION = "Can't found any invitation which you define!"
NOT_YOUR_INVITATION = "This invitation is not your!"
NOT_FOUND_PALLET = "Can't find any pallet with following ID!"
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
BRANCH_CHANGE_COMPANY = "You can't change company of branch to another company!"
NOT_FOUND_EMPLOYEE = "Can't find any of users who has a following access employee code!"
NOT_FOUND_USER = "Can't find any of users who has a following access user id!"
NOT_REQUEST_EMPLOYEE_CODE = "You didn't send employee code for create access!"
NOT_REQUEST_STORAGE_CODE = "You didn't send storage code for create access!"
NOT_FOUND_STATION = "Can't found any station with the following id!"
CAN_NOT_ACCEPT = "You don't have permission to accept it"
SENSOR_EXISTS = "You can't overide for any existed sensor!"
OLD_PASSWORD_INCORRECT = "Your old password is invalid!"
CAN_NOT_CHANGE_STORAGE_OF_SENSOR = "You can't change storage which have this sensor!"
NOT_FOUND_SENSOR = "You can't find any sensor with this id!"
DATA_NOT_FILLED = "You haven't filled a needed data for this api"
MUST_HAVE_STORAGE_ID = "You must have storage id for this API!"
CAN_NOT_CHANGE_STORAGE_OF_PALLET = "You can't change storage which save this pallet!"
INVALID_ROLE = "This role is invalid!"
NOT_CREATE_USER_ROLE = "You can't create user with this role! Because you don't have enough permissions"
CAN_NOT_DO_THIS_FEATURE = "You can't do this feature! Because it is blocking for secure problems"
ONLY_IS_ACITVE_IS_UPDATED = "You should update for only one field that is 'is_active'!"
CAN_NOT_ACTIVE = "You can't active for this user permission! Because you are not admin or employer of this account"
HAVE_STORAGE_ID_SUPERVISOR_OF = "You can't create supervisor without storage id!"
ONLY_OWNER_ADMIN = "Only owner or administrator can create role !"
DO_NOT_HAVE_PERMISSION = "All of your permissions do not have some permissions in this list which are provided by you!"
ONLY_OWNER_ADMIN_CREATE_USER = "You can't not create user because you are not admin or onwer!"
CREATE_USER_WITH_ROLE_BELOW_YOU = "You just create user with all role below you or created by you!"
DO_NOT_PERMISSION = "You don't have permissions to do this!"
ARE_NOT_OWNER = "You are not owner of this!"
NOT_FOUND_PERMISSION = "Can't find any permissions like that!"
ONLY_OWNER = "You must be owner to do it!"
ONLY_ADMIN = "You must be admin to do it!"
WAS_RECEIVED = "This permission was be blocked by you !"
NOT_FOUND_BLOCK = "Don't have any block requests like that!"
CAN_NOT_BLOCK_UNKNOW_PERMISSION = "You can't block the permission which is user not have!"
NOT_FOUND_BRANCH = "Can't find any branch following this ID!"
BRANCH_NOT_OWN = "You must be owner of this branch to do it!"
STORAGE_NOT_OWN = "You must be owner of this storage to do it!"
EMPLOYEE_NOT_OWN = "You must be owner of this employee to do it!"
CAN_NOT_CHANGE_ACCESS_EMPLOYEE = "You can't change employee of an access ticket!"
YOU_NOT_IN_STORAGE = "You are not serving any storage!"
YOU_NOT_IN_BRANCH_OR_STORAGE = "You are not serving any branch or storage!"
YOU_NOT_IN_BRANCH = "You are not serving any branch!"
AUTHENICATION_IN_IOT = "You can't do this because you don't have a account in IOT LAB"
NOT_FOUND_API = "Not found this API !"