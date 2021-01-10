from string import Template

oauth_template = Template(
    """
    {
       "access_token":"${access_token}",
       "client_id":"${client_id}",
       "client_secret":"${client_secret}",
       "refresh_token":"${refresh_token}",
       "token_expiry":"2020-10-27T18:03:48Z",
       "token_uri":"https://accounts.google.com/o/oauth2/token",
       "user_agent":null,
       "revoke_uri":"https://oauth2.googleapis.com/revoke",
       "id_token":null,
       "id_token_jwt":null,
       "token_response":{
          "access_token":"${refresh_token}",
          "expires_in": 3599,
          "scope":"https://www.googleapis.com/auth/youtube.upload",
          "token_type":"Bearer"
       },
       "scopes":[
          "https://www.googleapis.com/auth/youtube.upload"
       ],
       "token_info_uri":"https://oauth2.googleapis.com/tokeninfo",
       "invalid":false,
       "_class":"OAuth2Credentials",
       "_module":"oauth2client.client"
    }
            """

)
