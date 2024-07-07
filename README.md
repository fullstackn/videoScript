### User access token generation (facebook)

1. Register facebook developer, linked with target facebook profile
2. Go to https://developers.facebook.com/apps, press "Create App" button
3. Link with business portfolio, that is linked with target page and target instagram account
4. On next screen choose "Other - explore other products and data permissions such as ads management, WhatsApp and more." 
   You'll be asked to select an app type. After this you can add the permissions and products you need.
5. On next screen choose app type "Business"
6. Type any name, select business portfolio, press "Create App"
7. Setup products "Facebook Login for Business", "Instagram Graph API"
8. Go to https://developers.facebook.com/tools/explorer/
7. Choose newly created app, User or Page = 'Get User access token'. The following permissions are necessary:
   - publish_video
   - pages_show_list
   - business_management
   - instagram_basic
   - instagram_content_publish
   - pages_manage_posts
   Push Generate Access Token, copy token
8. Go to https://developers.facebook.com/tools/debug/accesstoken/, paste token to the field, push "Debug", check info.
9. Press "Extend Access token" in the bottom of the page
10. The whole process of user access token generation is also described here - https://elfsight.com/blog/how-to-get-facebook-access-token/
11. For scripts usage environment variable USER_FB_TOKEN should be assigned with value of generated access token
12. The whole process is pretty complicated, including linking up different facebook/instagram entities. This little manual does not claim to be fully accurate and complete; perhaps something is missing.

### User access token generation (Meta Threads)
1. Register facebook developer, linked with target facebook profile
2. Go to https://developers.facebook.com/apps, press "Create App" button
3. Link with business portfolio, that is linked with target page and target instagram account
4. On next screen choose "Access the Threads API" 
5. Choose any name, press "Create App"
6. Go to permissions, add "threads_content_publish"
7. Go to settings, add to "Redirect Callback URLs"  https://oauth.pstmn.io/v1/browser-callback
8. Go to postman.com account, in order to generate access_token.
9. Create GET request, https://graph.threads.net/access_token?grant_type=th_exchange_token
Params:
- grant_type=th_exchange_token
- client_secret - take from App
10. On "Authorization" tab fill fields:
- Header Prefix -access_token 
- Auth URL - https://threads.net/oauth/authorize
- Access Token URL - https://graph.threads.net/oauth/access_token
- Client ID - take from App
- Client Secret - take from App
- Scope - threads_basic,threads_content_publish
- Client Authentication - Send client credentials in body
11. Press "Get New Access Token". After authorization through threads page, press "Proceed" 
12. Copy user_id to corresponding placeholder in `threads.py` 
13. Press "Send" on request, copy your access token from returned body: 
```
{
    "access_token": "THQWJYdkZAvbVNDbDQyT...",
    "token_type": "bearer",
    "expires_in": 5174426
}
```
14. Copy `access_token` to corresponding placeholder in `threads.py`
15. This token expires in 60 days.

TODO
- snapchat
- whatsapp