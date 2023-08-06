from analyticCli import *

class AnalyticCache  (AnalyticCli):

    def __init__(self, host='localhost', port=15387, res='event'):
        super(AnalyticCache, self).__init__(host, port)


if __name__ == '__main__':
    host    = 'localhost'
    cache   = AnalyticCache(host, 15387)
    cache.connect()
    for res in ['timeseries', 'event', 'minute']:
        print '######', res, '######'
        print 'available analytics: ', cache.analytics(res)
        print 'nrows: ', cache.count(res,'anlrtns')
    #
    print "analytics::", cache.getAnalytic('minute','anlrtns')
    #
    print "minTime('timeseries', ['A1', 'B1'])::", cache.minTime('timeseries', ['A1', 'B1'])
    print "minTime'timeseries', ['anlrtns', 'anlcmntincr'])::", cache.minTime('timeseries', ['anlrtns', 'anlcmntincr'])
    print "maxTime('timeseries', ['A1', 'B1'])::", cache.maxTime('timeseries', ['A1', 'B1'])
    print "maxTime'timeseries', ['anlrtns', 'anlcmntwin'])::", cache.maxTime('timeseries', ['anlrtns', 'anlcmntwin'])
    #
    print "getAnalyticByTimeRange('minute', 'anlcmntincr')::\n", cache.getAnalyticByTimeRange('minute', 'B1')
    #print "getAnalyticByTimeRange('minute', 'idxmktcap')::\n", cache.getAnalyticByTimeRange('minute', 'anlrtns')
    #print 'getAnalyticByTimeRange\n', cache.v('minute', 'anlrtns', 
    #        cache.minTime('timeseries','anlrtns'),
    #        cache.minTime('timeseries','anlrtns') + timedelta(minutes=5), True)
    #