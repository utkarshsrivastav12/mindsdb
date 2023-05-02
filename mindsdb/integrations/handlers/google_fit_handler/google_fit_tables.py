from mindsdb.integrations.libs.api_handler import APITable
from mindsdb.integrations.libs.response import HandlerResponse as Response
from mindsdb.integrations.utilities.sql_utils import extract_comparison_conditions
from mindsdb_sql.parser import ast

class GoogleFitTable(APITable):
    def select(self, query: ast.Select) -> Response:

        conditions = extract_comparison_conditions(query.where)
        
        params = {}
        filters = []
        steps = {}
        for op, arg1, arg2 in conditions:

            if op == 'or':
                raise NotImplementedError(f'OR is not supported')
            if arg1 == 'date':
                date = time_parser(arg2)
                if op == '>':
                    params['start_time'] = date
                elif op == '<':
                    params['end_time'] = date
                else:
                    raise NotImplementedError
            else:
                raise NotImplementedError(f'This query is not supported')

        result = self.handler.call_twitter_api(
            method_name='get_steps',
            params=params
        )
        return result

    def get_columns(self):
        return [
            'id',
            'created_at',
            'text',
            'edit_history_tweet_ids',
            'author_id',
            'author_name',
            'author_username',
            'conversation_id',
            'in_reply_to_tweet_id',
            'in_retweeted_to_tweet_id',
            'in_quote_to_tweet_id',
            'in_reply_to_user_id',
            'in_reply_to_user_name',
            'in_reply_to_user_username',
        ]     