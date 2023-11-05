from datetime import datetime

from qiniu import Auth, put_file, etag, put_data, BucketManager
import qiniu.config


def upload_qiniu(filestorage):
    # 需要填写你的 Access Key 和 Secret Key
    access_key = 'VSRtzMjvuLNBjt3mnVsYr68eacBsf-cGjVgGSPJK'
    secret_key = 'brmU6CUY_UBmOJi_iwQ7Ji_dU6YRhzlaGNiQnLpd'
    # 构建鉴权对象
    q = Auth(access_key, secret_key)
    # 要上传的空间
    bucket_name = 'flskblog'
    # 上传后保存的文件名
    filename = filestorage.filename
    ran = datetime.now().strftime('%Y%m%d%H%M%S')
    suffix = filename.rsplit('.')[-1]    
    key = f"{filename.rsplit('.')[0]}_{ran}.{suffix}"
    # 生成上传 Token，可以指定过期时间等
    token = q.upload_token(bucket_name, key, 3600)
    # 要上传文件的本地路径
    # localfile = './sync/bbb.jpg'
    # ret, info = put_file(token, key, localfile)
    ret, info = put_data(up_token=token, key=key, data=filestorage.read())
    return ret, info


def delete_qiniu(filename):
    # 需要填写你的 Access Key 和 Secret Key
    access_key = 'VSRtzMjvuLNBjt3mnVsYr68eacBsf-cGjVgGSPJK'
    secret_key = 'brmU6CUY_UBmOJi_iwQ7Ji_dU6YRhzlaGNiQnLpd'
    # 构建鉴权对象
    q = Auth(access_key, secret_key)
    # 要上传的空间
    bucket_name = 'flskblog'
    # 初始化BucketManager
    bucket = BucketManager(q)
    # key就是要删除的文件的名字
    key = filename
    ret, info = bucket.delete(bucket_name, key)
    return info
