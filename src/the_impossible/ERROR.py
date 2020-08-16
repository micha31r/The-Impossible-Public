# A list of all errors:

SERVER_ERROR = {
	# Auth
	"AUTH_LOGIN"						:"Login failed",
	"AUTH_NO_USER"						:"User not found",
	"AUTH_PASSWORD"						:"Wrong password",
	"AUTH_PASSWORD_MATCH"				:"Password does not match",

	# Signup
	"AUTH_SIGNUP"						:"Sign up failed",
	"AUTH_SIGNUP_USERNAME"				:"Username can only include A-Z, 0-9 and _",
	"AUTH_SIGNUP_USERNAME_TAKEN"		:"Username is taken",
	"AUTH_SIGNUP_EMAIL_TAKEN"			:"Email is taken",
	"AUTH_CODE"							:"Incorrect verification code",

	# Access
	"ACCESS"							:"You don't have access",

	# Idea
	"IDEA"								:"Idea not found",

	# File
	"FILE"								:"Invalid file type",
	"FILE_INVALID_DELETE"				:"Invalid file type, file is deleted",
	"FILE_SIZE"							:"File size is too big",

	# Other/unknown
	"UNKNOWN"							:"We've encountered some issues (0v0)",
}