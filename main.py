import sys
import logging

from datetime import datetime, timedelta, timezone
from instagrapi import Client
from instagrapi.exceptions import LoginRequired
from emailNotify import *

ACCOUNT_USERNAME = "SummaryAppTest"
ACCOUNT_PASSWORD = "!854Jis"

logger = logging.getLogger()

def main():
    client = Client()
    login_user(client)

    get_media_after_datetime = getDateTimeIntervalFromCurrentDayUTC()

    friend_to_media = {}
    friends = getFriendsToInquire()
    for friend in friends:
        media = getMediaFromFriends(client, friend, get_media_after_datetime)
        friend_to_media[friend] = media

    #print(friend_to_media)
    content = buildEmailContentFromMap(friends, friend_to_media)
    #print(content)
    send_email(datetime.now().strftime("%m/%d/%Y"), content)

def buildEmailContentFromMap(friends, friend_to_media):
    content_str = ""
    for friend in friends:
        media = friend_to_media[friend]
        if media:
            content_str = content_str + friend + " has posted the following: " + '\n'
            for item in media:
                content_str = content_str + item['media_type'] + ":" + item['full_url']
                content_str = content_str + " posted at: " + item['taken_at'].strftime("%m/%d/%Y, %H:%M:%S") + '\n' + '\n'
    return content_str 

def getMediaFromFriends(client, friend, get_media_after_datetime):
    # gets instagram user id
    user_id = client.user_id_from_username(friend)

    # hardcoded to use private instagram api to get media
    medias = client.user_medias(user_id, 20, 0, True)

    # a list of media for this friend
    media_metadatas = []
    for media in medias:
        if media.taken_at > get_media_after_datetime:
        # photos and videos only
            if media.media_type == 1 or media.media_type == 2:
                # flatten and extra all the fields we are interested in
                #print(media)
                #print("=============================")
                media_metadata = {}
                if media.media_type == 1:
                    media_metadata['full_url'] = media.image_versions2.get('candidates')[0]['url']
                    media_metadata['media_type'] = "Photo"
                elif media.media_type == 2:
                    media_metadata['full_url'] = media.video_url
                    media_metadata['media_type'] = "Video"

                media_metadata['taken_at'] = media.taken_at
                media_metadata['thumbnail_url'] = media.thumbnail_url
                media_metadata['profile_pic_url'] = media.user.profile_pic_url
                media_metadatas.append(media_metadata)
    return media_metadatas


# for now this is hardcoded to 1 year because bonnie and steven are losers that don't post alot
def getDateTimeIntervalFromCurrentDayUTC():
    return datetime.now(timezone.utc) - timedelta(days=365)

# for now this is hardcoded bonnie steven and preston only
def getFriendsToInquire():
    friends = ["binglett_kitty", "steven.zhu", "prestonlwright", "gamestop"]
    return friends

def login_user(cl):
    """
    Attempts to login to Instagram using either the provided session information
    or the provided username and password.
    """

   # cl.login(ACCOUNT_USERNAME, ACCOUNT_PASSWORD)
   # cl.dump_settings("session.json")

    session = cl.load_settings("session.json")

    login_via_session = False
    login_via_pw = False

    if session:
        try:
            cl.set_settings(session)
            cl.login(ACCOUNT_USERNAME, ACCOUNT_PASSWORD)

            # check if session is valid
            try:
                cl.get_timeline_feed()
            except LoginRequired:
                logger.info("Session is invalid, need to login via username and password")

                old_session = cl.get_settings()

                # use the same device uuids across logins
                cl.set_settings({})
                cl.set_uuids(old_session["uuids"])

                cl.login(ACCOUNT_USERNAME, ACCOUNT_PASSWORD)
            login_via_session = True
        except Exception as e:
            logger.info("Couldn't login user using session information: %s" % e)

    if not login_via_session:
        try:
            logger.info("Attempting to login via username and password. username: %s" % ACCOUNT_USERNAME)
            if cl.login(ACCOUNT_USERNAME, ACCOUNT_PASSWORD):
                login_via_pw = True
        except Exception as e:
            logger.info("Couldn't login user using username and password: %s" % e)

    if not login_via_pw and not login_via_session:
        raise Exception("Couldn't login user with either password or session")

if __name__ == '__main__':
    main()
    sys.exit()
