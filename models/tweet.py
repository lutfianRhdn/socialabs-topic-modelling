from config.db import db2
import re
from datetime import datetime

class Tweet:
    def getTweetByIdStr(id_str_list):
        return db2.tweets.find(
            {"id_str": {"$in": id_str_list}},
            {"_id":0, "full_text": 1, "id_str": 1, "user_id_str": 1, "username" : 1, "conversation_id_str": 1, "tweet_url" : 1, "in_reply_to_screen_name" :1}
        )
    
    def classifyTweet(id_str, data):
        return db2.tweets.update_many(
            {"id_str": id_str},
            {"$set": {"topic": data}}
        )

    def getTweetByKeyword(keyword, start_date, end_date, limit):
        # Match stage to filter tweets by keyword
        match_stage = {
            '$match': {
                'full_text': {'$regex': keyword, '$options': 'i'}
            }
        }
        
        pipeline = [match_stage]

        # Add date filtering if both start_date and end_date are provided
        if start_date and end_date:
            start_datetime = datetime.strptime(f"{start_date} 00:00:00 +0000", "%Y-%m-%d %H:%M:%S %z")
            end_datetime = datetime.strptime(f"{end_date} 23:59:59 +0000", "%Y-%m-%d %H:%M:%S %z")
            print(f"Filtering tweets from {start_datetime} to {end_datetime}")
            
            add_fields_stage = {
                '$addFields': {
                    'parsed_date': {'$toDate': '$created_at'}
                }
            }
            match_date_stage = {
                '$match': {
                    'parsed_date': {'$gte': start_datetime, '$lte': end_datetime}
                }
            }

            pipeline.extend([add_fields_stage, match_date_stage])
        
        # Project stage to include only specific fields
        project_stage = {
            '$project': {
                '_id' : 0,
                'full_text': 1,
                'username': 1,
                'in_reply_to_screen_name': 1,
                'tweet_url': 1
            }
        }
        pipeline.append(project_stage)
        
        # Limit stage to limit the number of results
        pipeline.append({'$limit': limit})

        # Execute the aggregation pipeline
        cursor = db2.tweets.aggregate(pipeline)
        return list(cursor)