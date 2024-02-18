from src import stats
import sqlite3


def test_get_message_statistics():
    """
     Testing message type for each user from all messages 
    """
    result = stats.get_message_statistics()
    expected_result = {525360073: [{'message_type': 'Photo', 'total_count': 130},
                                   {'message_type': 'Text', 'total_count': 28}, 
                                   {'message_type': 'Round Video', 'total_count': 27},
                                   {'message_type': 'Audio', 'total_count': 8}, 
                                   {'message_type': 'Other', 'total_count': 3},
                                   {'message_type': 'Video', 'total_count': 3}], 
                           581357902: [{'message_type': 'Text', 'total_count': 111},
                                       {'message_type': 'Photo', 'total_count': 71},
                                       {'message_type': 'Audio', 'total_count': 37},
                                       {'message_type': 'Sticker', 'total_count': 23}, 
                                       {'message_type': 'Round Video', 'total_count': 17},
                                       {'message_type': 'Video', 'total_count': 13},
                                       {'message_type': 'Other', 'total_count': 10}],
                           350428128: [{'message_type': 'Text', 'total_count': 76},
                                       {'message_type': 'Photo', 'total_count': 10},
                                       {'message_type': 'Video', 'total_count': 9},
                                       {'message_type': 'Round Video', 'total_count': 4},
                                       {'message_type': 'Other', 'total_count': 3},
                                       {'message_type': 'Sticker', 'total_count': 3},
                                       {'message_type': 'Audio', 'total_count': 2}],
                          559433336: [{'message_type': 'Text', 'total_count': 67}, 
                                      {'message_type': 'Sticker', 'total_count': 32},
                                      {'message_type': 'Photo', 'total_count': 26},
                                      {'message_type': 'Video', 'total_count': 24},
                                      {'message_type': 'Round Video', 'total_count': 9},
                                      {'message_type': 'Audio', 'total_count': 7}],
                           None: [{'message_type': 'Other', 'total_count': 1}]}

    assert result == expected_result

def test_get_total_duration():
    """
    Testing total duration of all audio and round video messages
    """
    result = stats.get_total_duration()
    expected_result = {None: {'audio_duration': 0, 
                                'video_duration': 0},
                       350428128: {'audio_duration': 148.0, 
                                'video_duration': 183.066}, 
                       525360073: {'audio_duration': 78.0, 
                                       'video_duration': 173.889},                                 
                       559433336: {'audio_duration': 88.0, 
                                     'video_duration': 18.0},
                       581357902: {'audio_duration': 380.0, 
                                   'video_duration': 79.037}}
       
    assert result == expected_result

def test_get_top_message_types():
    """
    Testing calculate messages by type for each user and sort
    """
    result = stats.get_top_message_types()
    expected_result = [{'message_type': 'Text', 'message_count': 282}, 
                       {'message_type': 'Photo', 'message_count': 237}, 
                       {'message_type': 'Sticker', 'message_count': 58}, 
                       {'message_type': 'Round Video', 'message_count': 57}, 
                       {'message_type': 'Audio', 'message_count': 54}, 
                       {'message_type': 'Video', 'message_count': 49}, 
                       {'message_type': 'Other', 'message_count': 17}]
       
    assert result == expected_result

def test_get_top_message_types_date():
    """
    Testing calculate messages by type for each user per period 
    from start_date to end_date
    """
    start_date = '2024-01-06'
    end_date = '2024-01-07'
    result = stats.get_top_message_types_date(start_date, end_date)
    expected_result = [{'message_type': 'Text', 'message_count': 278}, 
                       {'message_type': 'Photo', 'message_count': 237}, 
                       {'message_type': 'Sticker', 'message_count': 58}, 
                       {'message_type': 'Round Video', 'message_count': 56}, 
                       {'message_type': 'Audio', 'message_count': 54}, 
                       {'message_type': 'Video', 'message_count': 47}, 
                       {'message_type': 'Other', 'message_count': 17}]    
    
    assert result == expected_result
    
def test_get_message_type_frequency_per_hour():
    """
    Testing calculated frequency of sending messages distincted by type for wach user
    (per hour per period from start_date to end_date)
    """
    start_date = '2024-01-06'
    end_date = '2024-01-07'
    result = {user_id: 
                {message_type: f'{frequency:.2f}' for message_type, frequency in user_data.items()} 
                for user_id, user_data in stats.get_message_type_frequency_per_hour(start_date, end_date).items()}
    expected_result = { None: {'Other': '0.04'}, 
                       350428128: {'Audio': '0.08', 
                                'Other': '0.12',
                                'Photo': '0.42',
                                'Round Video': '0.12',
                                'Sticker': '0.12',
                                'Text': '3.00',
                                'Video': '0.29'}, 
                       525360073: {'Audio': '0.33', 
                                       'Other': '0.12',
                                       'Photo': '5.42',
                                       'Round Video': '1.12',
                                       'Text': '1.17',
                                       'Video': '0.12'},                                  
                       559433336: {'Audio': '0.29', 
                                     'Photo': '1.08',
                                      'Round Video': '0.38',
                                     'Sticker': '1.33',
                                     'Text': '2.79',
                                     'Video': '1.00'},
                       581357902: {'Audio': '1.54', 
                                   'Other': '0.42',
                                   'Photo': '2.96',
                                   'Round Video': '0.71',
                                   'Sticker': '0.96',
                                   'Text': '4.62',
                                   'Video': '0.54'}}
       
    
    assert result == expected_result

def test_get_message_type_frequency_per_hour_nouser():
    """
    Testing calculated frequency of sending messages distincted by type  
    (per hour per period from start_date to end_date)
    """
    start_date = '2024-01-06'
    end_date = '2024-01-07'
    result  = stats.get_message_type_frequency_per_hour_nouser(start_date, end_date)
    result = {key: f'{value:.2f}' for key, value in result.items()}
    expected_result = {'Audio': '2.25', 
                       'Other': '0.71', 
                       'Photo': '9.88',
                       'Round Video': '2.33', 
                       'Sticker': '2.42',
                       'Text': '11.58',
                       'Video': '1.96'}
       
    
    assert result == expected_result    

def test_get_total_message_frequency_per_hour_all():
    """
    Testing calculated frequency of sending messages  
    (per hour per period from start_date to end_date)
    """
    start_date = '2024-01-06'
    end_date = '2024-01-07'
    result  = stats.get_total_message_frequency_per_hour_all(start_date, end_date)
    result = '{:.2f}'.format(result)
    expected_result = '31.12'
       
    
    assert result == expected_result  
    
