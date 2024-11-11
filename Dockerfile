FROM ruby:3
RUN mkdir /app
RUN mkdir /data
COPY ./androgee /app/androgee
WORKDIR /app/androgee
# RUN bundle install
ENTRYPOINT [ "ruby", "lib/main.rb" ]