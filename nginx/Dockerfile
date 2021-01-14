#uSE THE nginx image
FROM nginx 

#Remove the default nginx.conf
RUN rm /etc/nginx/conf.d/default.conf
RUN mkdir /etc/nginx/sites-enabled/

# Replace with our own nginx.conf
COPY nginx.conf /etc/nginx/conf.d/
COPY openvessel /etc/nginx/sites-enabled/
