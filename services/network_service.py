import socket

def get_local_ip():
    """
    بترجع IP الجهاز الحقيقي على الشبكة المحلية (مش 127.0.0.1).
    بترجع None لو الجهاز مش متصل بأي شبكة.
    """
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        # مش بيبعت أي بيانات فعلياً — بس بيستخدم لمعرفة الـ IP يلي رح يستخدمه النظام للخروج على الشبكة
        s.connect(('8.8.8.8', 80))
        ip = s.getsockname()[0]
        return ip
    except OSError:
        return None
    finally:
        s.close()