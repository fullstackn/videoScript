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

TODO
- threads
- tiktok
- snapchat
- whatsapp