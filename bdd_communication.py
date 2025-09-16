import os, json, re
from supabase import create_client, Client

f = open('secrets.json')
secrets = json.load(f)
supabase_key = secrets["SUPABASE-KEY"]
supabase_url = secrets["SUPABASE-URL"]
auth_email = secrets["USER_EMAIL"]
auth_pswrd = secrets["USER_PSWRD"]

class SupabaseDB:
    def __init__(self):
        self.supabase = None
    
    def auth_access_token(self, access_token : str):
        try:
            if self.check_auth():
                return True
            if self.supabase is None:
                self.supabase = create_client(supabase_url, supabase_key)
            
            res = self.supabase.auth.refresh_session(access_token)
            if res and res.session:
                return True
            return False
        except Exception as e:
            print(f"Sign-in failed: {e}")
            return False
    def auth_refresh_token(self, refresh_token):
        try:
            if self.check_auth():
                return True
            if self.supabase is None:
                self.supabase = create_client(supabase_url, supabase_key)
            
            res = self.supabase.auth.refresh_session(refresh_token)
            if res and res.session:
                return True
            return False
        except Exception as e:
            print(f"Sign-in failed: {e}")
            return False
    def auth_password(self, email, pswrd):
        try:
            if self.check_auth():
                return True
                
            # Create client if needed
            if self.supabase is None:
                self.supabase = create_client(supabase_url, supabase_key)
            
            # Sign in
            res = self.supabase.auth.sign_in_with_password({
                "email": email,
                "password": pswrd  
            })
            
            if res and res.session:
                return True, res.session.access_token, res.session.refresh_token
            else:
                return False
                
        except Exception as e:
            print(f"Sign-in failed: {e}")
            return False
    def check_auth(self):
        if self.supabase is None:
            return False
        try:
            session = self.supabase.auth.get_session()
            return session is not None
        except Exception as e:
            print(f"Auth check error: {e}")
            return False
    def getAllUser(self):
        response = (
            self.supabase.table("User")
            .select("*")
            .execute()
        )
        
        print(response.data)

    def getUser(self,userName : str):
        
        try:
            response = (
                self.supabase.table("User")
                .select("*")
                .eq("name", userName)
                .execute()
            )
            print(response.data)    
        except Exception as e:
            print(f"Query failed: {e}")

    def addPlaylist(self,name : str, audio_id : str):
        user_id = self.supabase.auth.get_user().user.id
        response = (
            self.supabase.table("Playlist")
            .insert({"name": name,"audio_id":audio_id, "user_id":user_id})
            .execute()
        )
        return response.data
    
    def getAllPlaylist(self) -> dict:
        user_id = self.supabase.auth.get_user().user.id
        response = (
            self.supabase.table("playlist_grouped_by_name")
            .select("*")
            .execute()
        )
        return response.data
    def getPlaylist(self, name : str):
        user_id = self.supabase.auth.get_user().user.id
        response = (
            self.supabase.table("Playlist")
            .select("*")
            .eq("user_id",user_id)
            .eq("name",name)
            .execute()
        )
        return response.data
    
    def deletePlaylist(self, name):
        user_id = self.supabase.auth.get_user().user.id
        response = (
            self.supabase.table("Playlist")
            .delete()
            .eq("user_id",user_id)
            .eq("name",name)
            .execute()
        )
        return response.data
    def deleteAllPlaylist(self):
        user_id = self.supabase.auth.get_user().user.id
        response = (
            self.supabase.table("Playlist")
            .delete()
            .eq("user_id",user_id)
            .execute()
        )
        return response.data
    def removeAudioFromPlaylist(self, name : str, audio_id : str):
        user_id = self.supabase.auth.get_user().user.id
        response = (
            self.supabase.table("Playlist")
            .delete()
            .eq("user_id",user_id)
            .eq("name",name)
            .eq("audio_id", audio_id)
            .execute()
        )
        return response.data
    def renamePlaylist(self, name : str, new_name : str):
        user_id = self.supabase.auth.get_user().user.id
        response = (
            self.supabase.table("Playlist")
            .update({"name" : new_name})
            .eq("user_id",user_id)
            .eq("name",name)
            .execute()
        )
        return response.data
    
    
    def addAudio(self, title : str, channel_name : str, video_id : str, url : str, duration : str):
        try:
            response = (
                self.supabase.table("Audio")
                .insert({"id":video_id,"title": title, "channel_name":channel_name,"duration":duration, "url":url, "audio":"0101"})
                .execute()
            )
            file_path = f"audio/{title}.webm"
            with open(file_path,"rb") as f:
                self.supabase.storage.from_("audio").upload(f"{video_id}.webm", f)
            return response.data, True
        except Exception as err:
            return err, False
    def getAllAudio(self):
        response = (
            self.supabase.table("Audio")
            .select("*")
            .execute()
        )
        return response.data
        