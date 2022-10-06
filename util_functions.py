#from math import floor

def emphasize_log_msg(msg, no_of_asterisks = 100, symbol = "*"):
        """
        Makes a msg appear like that:
        
        ****************************************************************************************************
        msg
        ****************************************************************************************************
        
        """
        return( "\n" + symbol*no_of_asterisks + "\n"+  msg +"\n" +symbol*no_of_asterisks  )


def which_width_to_start_from_to_align_in_center(
        objects_width_rate:float, 
        windows_width:int
        ) -> dict:
    
    objects_width = round(objects_width_rate * windows_width)
    should_start_from = round((windows_width/2) - (objects_width/2))

    return {"objects_width":objects_width, "should_start_from": should_start_from}


def which_width_to_start_from_to_align_in_center_absolute_number(
        objects_width:float, 
        windows_width:int
        ) -> dict:
    
    should_start_from = round((windows_width - objects_width)/2) 
    
    return {"objects_width":objects_width, "should_start_from": should_start_from}


def displace_subs(
    srt_file = "../8.Simple.Rules.S01E03.WEBRip.x264-ION10.srt",
    displace_to_earlier = True, #If false, to a later moment
    seconds:int = 3 #**kwargs
    ):

    with open(srt_file, 'r',encoding = 'utf-8') as s:
        text_of_srt_file = s.read()

    # Parse lines as srt
    subs = list(srt.parse( text_of_srt_file ))

    timediff = datetime.timedelta(seconds = 3 ) 

    for sub in subs:

        if displace_to_earlier:
            sub.start = sub.start - timediff
            sub.end = sub.end - timediff
        else:
            sub.start = sub.start + timediff
            sub.end = sub.end + timediff

    with open("../shifted_srt.srt",'w',encoding = 'utf-8') as new_srt:
        new_srt.write(srt.compose(subs))
    