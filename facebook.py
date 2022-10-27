# Temporary solution from Laura Miguel
# (https://github.com/medialab/ural/pull/117/files#diff-190c4fd74eeecad95f9253d1ea7516b1cbe6f8135f72e692cf9a39b90665ff39)
# Can be deleted and removed from parse_url() when Minet is updated with solution

def contains_id(url):
    if '/permalink.php' in url and '&id=' in url \
        or '/story.php' in url and '&id=' in url \
        or '/posts/' in url \
        or '/permalink/' in url \
        or '/groups/' in url:
        return True
   