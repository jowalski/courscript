def str_mlsec(time):
    return(time.strftime('%H:%M:%S.%f')[:-3])


def format_start_end(start, end):
    return(u'{0} - {1}'.format(str_mlsec(start), str_mlsec(end)))
