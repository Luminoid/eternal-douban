def get_user_url(col_type, user_id):
    return 'https://%s.douban.com/people/%s/' % (col_type, user_id)


def get_api_url(col_type, col_id):
    return 'https://api.douban.com/v2/%s/subject/%s' % (col_type, col_id)
