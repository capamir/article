from kavenegar import *


def send_otp_code(phone_number, code):
    try:
        api = KavenegarAPI('2F635471583036423133653875524B4830364D5969674F67795877334148564973614732746A46483455383D')
        params = {
            'sender': '',#optional
            'receptor': phone_number,
            'message': f'کد تایید شما {code }',
        }
        
        response = api.sms_send(params)
        print(response)
    except APIException as e: 
        print(e)
    except HTTPException as e: 
        print(e)


# send_otp_code("09335522639", 8888)