import os
import sys
import unittest

log_analyzer_path = '/Development/virtualenvs/miiscanLogAnalyzer/src/log_analyzer'
sys.path.append(log_analyzer_path)

from handler.filter import *

class JbossEjbFilterTestCase(unittest.TestCase):
    """ Testing log filter
        *** filtering words from jboss log
            "INFO", "WARN", "ERROR", "DEBUG", "fail", stacktraces

        - test to find the words from the log file
    """


    def setUp(self):
        self.filtering_words = ["INFO", "WARN", "ERROR", "DEBUG", "fail", "        at"]
        self.log_dump = """2012-10-02 00:00:43,907 DEBUG [org.jboss.ejb.plugins.AbstractInstanceCache] (Timer-1)  removePassivated, now=1349136043907, maxLifeAfterPassivation=1200000
2012-10-02 00:00:43,907 DEBUG [org.jboss.ejb.plugins.LRUEnterpriseContextCachePolicy] (Timer-1)  RemoverTask, done
2012-10-02 00:00:47,220 DEBUG [org.jboss.modcluster.ModClusterService] (ContainerBackgroundProcessor[StandardEngine[jboss.web]])  Check status for engine [jboss.web]
2012-10-02 00:00:57,221 DEBUG [org.jboss.modcluster.ModClusterService] (ContainerBackgroundProcessor[StandardEngine[jboss.web]])  Check status for engine [jboss.web]
2012-10-02 00:01:07,221 DEBUG [org.jboss.modcluster.ModClusterService] (ContainerBackgroundProcessor[StandardEngine[jboss.web]])  Check status for engine [jboss.web]
2012-10-02 00:01:17,221 DEBUG [org.jboss.modcluster.ModClusterService] (ContainerBackgroundProcessor[StandardEngine[jboss.web]])  Check status for engine [jboss.web]
2012-10-02 00:01:27,221 DEBUG [org.jboss.modcluster.ModClusterService] (ContainerBackgroundProcessor[StandardEngine[jboss.web]])  Check status for engine [jboss.web]
2012-10-02 00:01:32,059 DEBUG [org.jboss.remoting.transport.socket.ServerThread] (WorkerThread#2[192.168.20.71:50681])  WorkerThread#2[192.168.20.71:50681] closed socketWrapper: ServerSocketWrapper[Socket[addr=/192.168.20.71,port=50681,localport=3873].11b75468]
2012-10-02 00:01:32,073 DEBUG [org.jboss.ejb3.stateless.StatelessContainer] (WorkerThread#1[192.168.20.71:50682])  Received dynamic invocation for method with hash: 5933660363302521807
2012-10-02 00:01:32,080 INFO  [com.riavera.ejb.session.MobileDeviceBean] (WorkerThread#1[192.168.20.71:50682])  authenticating device: [com.riavera.misc.Pair@358a4791, com.riavera.misc.Pair@9609c0d, com.riavera.misc.Pair@25a51e4a, com.riavera.misc.Pair@7b679f94, com.riavera.m
isc.Pair@501decd7]
2012-10-02 00:01:32,081 DEBUG [com.riavera.ejb.session.MobileDeviceBean] (WorkerThread#1[192.168.20.71:50682]) ::nnapp_fi_in::99: found parameter: OS=IOS
2012-10-02 00:01:32,081 DEBUG [com.riavera.ejb.session.MobileDeviceBean] (WorkerThread#1[192.168.20.71:50682]) ::nnapp_fi_in::99: found parameter: MODEL=iPhone
2012-10-02 00:01:32,081 DEBUG [com.riavera.ejb.session.MobileDeviceBean] (WorkerThread#1[192.168.20.71:50682]) ::nnapp_fi_in::99: found parameter: IMEI=c235fcfaa081c1af8324a46a1951606e
2012-10-02 00:01:32,081 DEBUG [com.riavera.ejb.session.MobileDeviceBean] (WorkerThread#1[192.168.20.71:50682]) ::nnapp_fi_in::99: found parameter: BRAND=FU
2012-10-02 00:01:32,081 DEBUG [com.riavera.ejb.session.MobileDeviceBean] (WorkerThread#1[192.168.20.71:50682]) ::nnapp_fi_in::99: found parameter: OS_VERSION=iPhone OS 6.0
2012-10-02 00:01:32,081 WARN  [com.riavera.ejb.session.MobileDeviceBean] (WorkerThread#1[192.168.20.71:50682]) ::nnapp_fi_in::99: extra device attribute supplied but not processed: OS=IOS
2012-10-02 00:01:32,081 WARN  [com.riavera.ejb.session.MobileDeviceBean] (WorkerThread#1[192.168.20.71:50682]) ::nnapp_fi_in::99: extra device attribute supplied but not processed: MODEL=iPhone
2012-10-02 00:01:32,081 WARN  [com.riavera.ejb.session.MobileDeviceBean] (WorkerThread#1[192.168.20.71:50682]) ::nnapp_fi_in::99: extra device attribute supplied but not processed: BRAND=FU
2012-10-02 00:01:32,081 WARN  [com.riavera.ejb.session.MobileDeviceBean] (WorkerThread#1[192.168.20.71:50682]) ::nnapp_fi_in::99: extra device attribute supplied but not processed: OS_VERSION=iPhone OS 6.0
2012-10-02 00:01:32,081 INFO  [com.riavera.ejb.session.MobileDeviceBean] (WorkerThread#1[192.168.20.71:50682]) ::nnapp_fi_in::99: got device id params: serialKey='IMEI:c235fcfaa081c1af8324a46a1951606e'
2012-10-02 00:01:32,081 DEBUG [org.hibernate.impl.SessionImpl] (WorkerThread#1[192.168.20.71:50682]) ::nnapp_fi_in::99: opened session at timestamp: 5526061433163776
2012-10-02 00:01:32,081 DEBUG [org.hibernate.ejb.AbstractEntityManagerImpl] (WorkerThread#1[192.168.20.71:50682]) ::nnapp_fi_in::99: Looking for a JTA transaction to join
2012-10-02 00:01:32,081 DEBUG [org.hibernate.jdbc.JDBCContext] (WorkerThread#1[192.168.20.71:50682]) ::nnapp_fi_in::99: successfully registered Synchronization
2012-10-02 00:01:32,081 DEBUG [org.hibernate.ejb.AbstractEntityManagerImpl] (WorkerThread#1[192.168.20.71:50682]) ::nnapp_fi_in::99: Looking for a JTA transaction to join
2012-10-02 00:01:32,081 DEBUG [org.hibernate.ejb.AbstractEntityManagerImpl] (WorkerThread#1[192.168.20.71:50682]) ::nnapp_fi_in::99: Transaction already joined
2012-10-02 00:01:32,081 DEBUG [org.hibernate.jdbc.AbstractBatcher] (WorkerThread#1[192.168.20.71:50682]) ::nnapp_fi_in::99: about to open PreparedStatement (open PreparedStatements: 0, globally: 0)
2012-10-02 00:01:32,081 DEBUG [org.hibernate.jdbc.ConnectionManager] (WorkerThread#1[192.168.20.71:50682]) ::nnapp_fi_in::99: opening JDBC connection
2012-10-02 00:01:32,082 DEBUG [org.hibernate.SQL] (WorkerThread#1[192.168.20.71:50682]) ::nnapp_fi_in::99: select custmobile0_.CUST_MOBILE_GUID as CUST1_127_, custmobile0_.BRAND as BRAND127_, custmobile0_.CUST_GUID as CUST3_127_, custmobile0_.ENTRY_DATE as ENTRY4_127_, custmo
bile0_.LOCATION as LOCATION127_, custmobile0_.MODEL as MODEL127_, custmobile0_.NETWORK_OPERATOR as NETWORK7_127_, custmobile0_.NETWORK_OPERATOR_COUNTRY as NETWORK8_127_, custmobile0_.OS as OS127_, custmobile0_.OS_VERSION as OS10_127_, custmobile0_.PHONE_NUM as PHONE11_127_, c
ustmobile0_.SERIAL_NO as SERIAL12_127_, custmobile0_.STATE as STATE127_, custmobile0_.VALIDATED as VALIDATED127_, custmobile0_.VALIDATION_DATE as VALIDATION15_127_, custmobile0_.VALIDATION_DETAIL as VALIDATION16_127_, custmobile0_.VERSION as VERSION127_ from offnet.CUST_MOBIL
E custmobile0_ where custmobile0_.SERIAL_NO=?
2012-10-02 00:01:32,082 DEBUG [org.hibernate.jdbc.AbstractBatcher] (WorkerThread#1[192.168.20.71:50682]) ::nnapp_fi_in::99: about to open ResultSet (open ResultSets: 0, globally: 0)
2012-10-02 00:01:32,082 DEBUG [org.hibernate.loader.Loader] (WorkerThread#1[192.168.20.71:50682]) ::nnapp_fi_in::99: result row: EntityKey[com.riavera.ejb.entity.CustMobile#402894c737509bab013784ca2e0703a3]
2012-10-02 00:01:32,083 DEBUG [org.hibernate.jdbc.AbstractBatcher] (WorkerThread#1[192.168.20.71:50682]) ::nnapp_fi_in::99: about to close ResultSet (open ResultSets: 1, globally: 1)
2012-10-02 00:01:32,083 DEBUG [org.hibernate.jdbc.AbstractBatcher] (WorkerThread#1[192.168.20.71:50682]) ::nnapp_fi_in::99: about to close PreparedStatement (open PreparedStatements: 1, globally: 1)
2012-10-02 00:01:32,083 DEBUG [org.hibernate.jdbc.ConnectionManager] (WorkerThread#1[192.168.20.71:50682]) ::nnapp_fi_in::99: aggressively releasing JDBC connection
2012-10-02 00:01:32,083 DEBUG [org.hibernate.jdbc.ConnectionManager] (WorkerThread#1[192.168.20.71:50682]) ::nnapp_fi_in::99: releasing JDBC connection [ (open PreparedStatements: 0, globally: 0) (open ResultSets: 0, globally: 0)]
2012-10-02 00:01:32,083 DEBUG [org.hibernate.engine.TwoPhaseLoad] (WorkerThread#1[192.168.20.71:50682]) ::nnapp_fi_in::99: resolving associations for [com.riavera.ejb.entity.CustMobile#402894c737509bab013784ca2e0703a3]
2012-10-02 00:01:32,083 DEBUG [org.hibernate.engine.TwoPhaseLoad] (WorkerThread#1[192.168.20.71:50682]) ::nnapp_fi_in::99: done materializing entity [com.riavera.ejb.entity.CustMobile#402894c737509bab013784ca2e0703a3]
2012-10-02 00:01:32,083 DEBUG [org.hibernate.engine.StatefulPersistenceContext] (WorkerThread#1[192.168.20.71:50682]) ::nnapp_fi_in::99: initializing non-lazy collections
2012-10-02 00:01:32,083 INFO  [com.riavera.ejb.session.MobileDeviceBean] (WorkerThread#1[192.168.20.71:50682]) ::nnapp_fi_in::99: found 1 entries matching device serial key: IMEI:c235fcfaa081c1af8324a46a1951606e
2012-10-02 00:01:32,083 DEBUG [org.hibernate.event.def.AbstractSaveEventListener] (WorkerThread#1[192.168.20.71:50682]) ::nnapp_fi_in::99: generated identifier: 402894c739f907ec013a1ec70bb30705, using strategy: org.hibernate.id.UUIDHexGenerator
2012-10-02 00:01:32,083 DEBUG [org.hibernate.event.def.AbstractFlushingEventListener] (WorkerThread#1[192.168.20.71:50682]) ::nnapp_fi_in::99: processing flush-time cascades
2012-10-02 00:01:32,083 DEBUG [org.hibernate.event.def.AbstractFlushingEventListener] (WorkerThread#1[192.168.20.71:50682]) ::nnapp_fi_in::99: dirty checking collections
2012-10-02 00:01:32,083 DEBUG [org.hibernate.event.def.AbstractFlushingEventListener] (WorkerThread#1[192.168.20.71:50682]) ::nnapp_fi_in::99: Flushed: 1 insertions, 0 updates, 0 deletions to 2 objects
2012-10-02 00:01:32,083 DEBUG [org.hibernate.event.def.AbstractFlushingEventListener] (WorkerThread#1[192.168.20.71:50682]) ::nnapp_fi_in::99: Flushed: 0 (re)creations, 0 updates, 0 removals to 0 collections
2012-10-02 00:01:32,083 DEBUG [org.hibernate.pretty.Printer] (WorkerThread#1[192.168.20.71:50682]) ::nnapp_fi_in::99: listing entities:
2012-10-02 00:01:32,083 DEBUG [org.hibernate.pretty.Printer] (WorkerThread#1[192.168.20.71:50682]) ::nnapp_fi_in::99: com.riavera.ejb.entity.CustMobileHistory{lastUseDate=2012-10-02 00:01:32.083, location=null, networkOperatorCountry=null, networkOperator=null, entryDate=2012
-10-02 00:01:32.083, useCount=0, custMobileGuid=402894c737509bab013784ca2e0703a3, version=0, serialNo=IMEI:c235fcfaa081c1af8324a46a1951606e, custMobileHistoryGuid=402894c739f907ec013a1ec70bb30705, phoneNum=null, simOperator=null, simCountry=null}
2012-10-02 00:01:32,084 DEBUG [org.hibernate.jdbc.AbstractBatcher] (WorkerThread#1[192.168.20.71:50682]) ::nnapp_fi_in::99: about to open PreparedStatement (open PreparedStatements: 0, globally: 0)
2012-10-02 00:01:32,084 DEBUG [org.hibernate.jdbc.ConnectionManager] (WorkerThread#1[192.168.20.71:50682]) ::nnapp_fi_in::99: opening JDBC connection
2012-10-02 00:01:32,084 DEBUG [org.hibernate.SQL] (WorkerThread#1[192.168.20.71:50682]) ::nnapp_fi_in::99: insert into offnet.CUST_MOBILE_HISTORY (CUST_MOBILE_GUID, ENTRY_DATE, LAST_USE_DATE, LOCATION, NETWORK_OPERATOR, NETWORK_OPERATOR_COUNTRY, PHONE_NUM, SERIAL_NO, SIM_COUN
TRY, SIM_OPERATOR, USE_COUNT, VERSION, CUST_MOBILE_HISTORY_GUID) values (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
2012-10-02 00:01:32,084 DEBUG [org.hibernate.jdbc.AbstractBatcher] (WorkerThread#1[192.168.20.71:50682]) ::nnapp_fi_in::99: Executing batch size: 1
2012-10-02 00:01:32,084 DEBUG [org.hibernate.jdbc.Expectations] (WorkerThread#1[192.168.20.71:50682]) ::nnapp_fi_in::99: success of batch update unknown: 0
2012-10-02 00:01:32,084 DEBUG [org.hibernate.jdbc.AbstractBatcher] (WorkerThread#1[192.168.20.71:50682]) ::nnapp_fi_in::99: about to close PreparedStatement (open PreparedStatements: 1, globally: 1)
2012-10-02 00:01:32,084 DEBUG [org.hibernate.jdbc.ConnectionManager] (WorkerThread#1[192.168.20.71:50682]) ::nnapp_fi_in::99: skipping aggressive-release due to flush cycle
2012-10-02 00:01:32,084 DEBUG [org.hibernate.jdbc.ConnectionManager] (WorkerThread#1[192.168.20.71:50682]) ::nnapp_fi_in::99: aggressively releasing JDBC connection
2012-10-02 00:01:32,084 DEBUG [org.hibernate.jdbc.ConnectionManager] (WorkerThread#1[192.168.20.71:50682]) ::nnapp_fi_in::99: releasing JDBC connection [ (open PreparedStatements: 0, globally: 0) (open ResultSets: 0, globally: 0)]
2012-10-02 00:01:32,085 DEBUG [org.jboss.jpa.deployment.ManagedEntityManagerFactory] (WorkerThread#1[192.168.20.71:50682]) ::nnapp_fi_in::99: ************** closing entity managersession **************
2012-10-02 00:01:32,094 DEBUG [org.jboss.remoting.transport.socket.ServerThread] (WorkerThread#1[192.168.20.71:50682])  WorkerThread#1[192.168.20.71:50682] closed socketWrapper: ServerSocketWrapper[Socket[addr=/192.168.20.71,port=50682,localport=3873].237eb2bb]
2012-10-02 00:01:32,108 DEBUG [com.navahonetworks.ejb.session.app.LoginUserLogicBean] (WorkerThread#5[192.168.20.71:10806])  looking up LoginUserSF object by handle
2012-10-02 00:01:32,109 DEBUG [org.jboss.ejb.plugins.AbstractInstanceCache] (WorkerThread#5[192.168.20.71:10806])  Activation failure: javax.ejb.EJBException: Could not activate; failed to restore state
        at org.jboss.ejb.plugins.StatefulSessionFilePersistenceManager.activateSession(StatefulSessionFilePersistenceManager.java:343) [:6.1.0.Final]
        at org.jboss.ejb.plugins.StatefulSessionInstanceCache.activate(StatefulSessionInstanceCache.java:113) [:6.1.0.Final]
        at org.jboss.ejb.plugins.AbstractInstanceCache.doActivate(AbstractInstanceCache.java:458) [:6.1.0.Final]
        at org.jboss.ejb.plugins.StatefulSessionInstanceCache.doActivate(StatefulSessionInstanceCache.java:129) [:6.1.0.Final]
        at org.jboss.ejb.plugins.AbstractInstanceCache.get(AbstractInstanceCache.java:123) [:6.1.0.Final]
        at org.jboss.ejb.StatefulSessionContainer.getEJBObject(StatefulSessionContainer.java:394) [:6.1.0.Final]
        at sun.reflect.GeneratedMethodAccessor3683.invoke(Unknown Source) [:1.6.0_33]
        at sun.reflect.DelegatingMethodAccessorImpl.invoke(DelegatingMethodAccessorImpl.java:25) [:1.6.0_33]
        at java.lang.reflect.Method.invoke(Method.java:597) [:1.6.0_33]
        at org.jboss.invocation.Invocation.performCall(Invocation.java:386) [:6.1.0.Final]
        at org.jboss.ejb.StatefulSessionContainer$ContainerInterceptor.invokeHome(StatefulSessionContainer.java:564) [:6.1.0.Final]
        at org.jboss.ejb.plugins.StatefulSessionSecurityInterceptor.invokeHome(StatefulSessionSecurityInterceptor.java:97) [:6.1.0.Final]
        at org.jboss.ejb.plugins.SecurityInterceptor.process(SecurityInterceptor.java:270) [:6.1.0.Final]
        at org.jboss.ejb.plugins.SecurityInterceptor.invokeHome(SecurityInterceptor.java:205) [:6.1.0.Final]
        at org.jboss.resource.connectionmanager.CachedConnectionInterceptor.invokeHome(CachedConnectionInterceptor.java:178) [:6.1.0.Final]
        at org.jboss.ejb.plugins.StatefulSessionInstanceInterceptor.invokeHome(StatefulSessionInstanceInterceptor.java:127) [:6.1.0.Final]
        at org.jboss.ejb.plugins.CallValidationInterceptor.invokeHome(CallValidationInterceptor.java:56) [:6.1.0.Final]
        at org.jboss.ejb.plugins.AbstractTxInterceptor.invokeNext(AbstractTxInterceptor.java:125) [:6.1.0.Final]
        at org.jboss.ejb.plugins.TxInterceptorCMT.runWithTransactions(TxInterceptorCMT.java:350) [:6.1.0.Final]
        at org.jboss.ejb.plugins.TxInterceptorCMT.invokeHome(TxInterceptorCMT.java:161) [:6.1.0.Final]
        at org.jboss.ejb.plugins.security.PreSecurityInterceptor.process(PreSecurityInterceptor.java:160) [:6.1.0.Final]
        at org.jboss.ejb.plugins.security.PreSecurityInterceptor.invokeHome(PreSecurityInterceptor.java:91) [:6.1.0.Final]
        at org.jboss.ejb.plugins.LogInterceptor.invokeHome(LogInterceptor.java:132) [:6.1.0.Final]
        at org.jboss.ejb.plugins.ProxyFactoryFinderInterceptor.invokeHome(ProxyFactoryFinderInterceptor.java:107) [:6.1.0.Final]
        at org.jboss.ejb.SessionContainer.internalInvokeHome(SessionContainer.java:639) [:6.1.0.Final]
        at org.jboss.ejb.Container.invoke(Container.java:1089) [:6.1.0.Final]
        at sun.reflect.GeneratedMethodAccessor3461.invoke(Unknown Source) [:1.6.0_33]
        at sun.reflect.DelegatingMethodAccessorImpl.invoke(DelegatingMethodAccessorImpl.java:25) [:1.6.0_33]
        at java.lang.reflect.Method.invoke(Method.java:597) [:1.6.0_33]
        at org.jboss.mx.interceptor.ReflectedDispatcher.invoke(ReflectedDispatcher.java:157) [:6.0.0.GA]
        at org.jboss.mx.server.Invocation.dispatch(Invocation.java:96) [:6.0.0.GA]
        at org.jboss.mx.server.Invocation.invoke(Invocation.java:88) [:6.0.0.GA]
        at org.jboss.mx.server.AbstractMBeanInvoker.invoke(AbstractMBeanInvoker.java:271) [:6.0.0.GA]
        at org.jboss.mx.server.MBeanServerImpl.invoke(MBeanServerImpl.java:670) [:6.0.0.GA]
        at org.jboss.invocation.local.LocalInvoker$MBeanServerAction.invoke(LocalInvoker.java:169) [:6.1.0.Final]
        at org.jboss.invocation.local.LocalInvoker.invoke(LocalInvoker.java:118) [:6.1.0.Final]
        at org.jboss.invocation.InvokerInterceptor.invokeLocal(InvokerInterceptor.java:209) [:6.1.0.Final]
        at org.jboss.invocation.InvokerInterceptor.invoke(InvokerInterceptor.java:195) [:6.1.0.Final]
        at org.jboss.proxy.TransactionInterceptor.invoke(TransactionInterceptor.java:61) [:6.1.0.Final]
        at org.jboss.proxy.ejb.SecurityContextInterceptor.invoke(SecurityContextInterceptor.java:64) [:6.1.0.Final]
        at org.jboss.proxy.SecurityInterceptor.invoke(SecurityInterceptor.java:68) [:6.1.0.Final]
        at org.jboss.proxy.ejb.HomeInterceptor.invoke(HomeInterceptor.java:184) [:6.1.0.Final]
        at org.jboss.proxy.ClientContainer.invoke(ClientContainer.java:101) [:6.1.0.Final]
        at org.jboss.proxy.ejb.handle.StatefulHandleImpl.getEjbObjectViaJndi(StatefulHandleImpl.java:255) [:6.1.0.Final]
        at org.jboss.proxy.ejb.handle.StatefulHandleImpl.getEJBObject(StatefulHandleImpl.java:189) [:6.1.0.Final]
        at com.navahonetworks.ejb.session.app.LoginUserLogicBean.getLoginUserSF(LoginUserLogicBean.java:151) [:]
        at com.navahonetworks.ejb.session.app.LoginUserLogicBean.setUserContext(LoginUserLogicBean.java:891) [:]
        at sun.reflect.GeneratedMethodAccessor3877.invoke(Unknown Source) [:1.6.0_33]
        at sun.reflect.DelegatingMethodAccessorImpl.invoke(DelegatingMethodAccessorImpl.java:25) [:1.6.0_33]
        at java.lang.reflect.Method.invoke(Method.java:597) [:1.6.0_33]
        at org.jboss.invocation.Invocation.performCall(Invocation.java:386) [:6.1.0.Final]
        at org.jboss.ejb.StatelessSessionContainer$ContainerInterceptor.invoke(StatelessSessionContainer.java:233) [:6.1.0.Final]
        at org.jboss.resource.connectionmanager.CachedConnectionInterceptor.invoke(CachedConnectionInterceptor.java:156) [:6.1.0.Final]
        at org.jboss.ejb.plugins.StatelessSessionInstanceInterceptor.invoke(StatelessSessionInstanceInterceptor.java:173) [:6.1.0.Final]
        at org.jboss.ejb.plugins.CallValidationInterceptor.invoke(CallValidationInterceptor.java:63) [:6.1.0.Final]
        at org.jboss.ejb.plugins.AbstractTxInterceptor.invokeNext(AbstractTxInterceptor.java:121) [:6.1.0.Final]
        at org.jboss.ejb.plugins.TxInterceptorCMT.runWithTransactions(TxInterceptorCMT.java:350) [:6.1.0.Final]
        at org.jboss.ejb.plugins.TxInterceptorCMT.invoke(TxInterceptorCMT.java:181) [:6.1.0.Final]
        at org.jboss.ejb.plugins.SecurityInterceptor.process(SecurityInterceptor.java:268) [:6.1.0.Final]
        at org.jboss.ejb.plugins.SecurityInterceptor.invoke(SecurityInterceptor.java:211) [:6.1.0.Final]
        at org.jboss.ejb.plugins.security.PreSecurityInterceptor.process(PreSecurityInterceptor.java:158) [:6.1.0.Final]
        at org.jboss.ejb.plugins.security.PreSecurityInterceptor.invoke(PreSecurityInterceptor.java:84) [:6.1.0.Final]
        at org.jboss.ejb.plugins.LogInterceptor.invoke(LogInterceptor.java:205) [:6.1.0.Final]
        at org.jboss.ejb.plugins.ProxyFactoryFinderInterceptor.invoke(ProxyFactoryFinderInterceptor.java:138) [:6.1.0.Final]
        at org.jboss.ejb.SessionContainer.internalInvoke(SessionContainer.java:650) [:6.1.0.Final]
        at org.jboss.ejb.Container.invoke(Container.java:1072) [:6.1.0.Final]
        at sun.reflect.GeneratedMethodAccessor3461.invoke(Unknown Source) [:1.6.0_33]
        at sun.reflect.DelegatingMethodAccessorImpl.invoke(DelegatingMethodAccessorImpl.java:25) [:1.6.0_33]
        at java.lang.reflect.Method.invoke(Method.java:597) [:1.6.0_33]
        at org.jboss.mx.interceptor.ReflectedDispatcher.invoke(ReflectedDispatcher.java:157) [:6.0.0.GA]
        at org.jboss.mx.server.Invocation.dispatch(Invocation.java:96) [:6.0.0.GA]
        at org.jboss.mx.server.Invocation.invoke(Invocation.java:88) [:6.0.0.GA]
        at org.jboss.mx.server.AbstractMBeanInvoker.invoke(AbstractMBeanInvoker.java:271) [:6.0.0.GA]
        at org.jboss.mx.server.MBeanServerImpl.invoke(MBeanServerImpl.java:670) [:6.0.0.GA]
        at org.jboss.invocation.unified.server.UnifiedInvoker.invoke(UnifiedInvoker.java:232) [:6.1.0.Final]
        at org.jboss.remoting.ServerInvoker.invoke(ServerInvoker.java:967) [:6.1.0.Final]
        at org.jboss.remoting.transport.socket.ServerThread.completeInvocation(ServerThread.java:791) [:6.1.0.Final]
        at org.jboss.remoting.transport.socket.ServerThread.processInvocation(ServerThread.java:744) [:6.1.0.Final]
        at org.jboss.remoting.transport.socket.ServerThread.dorun(ServerThread.java:548) [:6.1.0.Final]
        at org.jboss.remoting.transport.socket.ServerThread.run(ServerThread.java:234) [:6.1.0.Final]
Caused by: java.io.FileNotFoundException: /usr/local/java/jboss-6.1.0.Final/server/prod.ejb/tmp/sessions/LoginUserSF-h7rxw4f1-p6/h7s6anht-pg.ser (No such file or directory)
        at java.io.FileInputStream.open(Native Method) [:1.6.0_33]
        at java.io.FileInputStream.<init>(FileInputStream.java:120) [:1.6.0_33]
        at org.jboss.ejb.plugins.StatefulSessionFilePersistenceManager$FISAction.run(StatefulSessionFilePersistenceManager.java:526) [:6.1.0.Final]
        at java.security.AccessController.doPrivileged(Native Method) [:1.6.0_33]
        at org.jboss.ejb.plugins.StatefulSessionFilePersistenceManager$FISAction.open(StatefulSessionFilePersistenceManager.java:535) [:6.1.0.Final]
        at org.jboss.ejb.plugins.StatefulSessionFilePersistenceManager.activateSession(StatefulSessionFilePersistenceManager.java:323) [:6.1.0.Final]
        ... 79 more

2012-10-02 00:01:32,113 ERROR [org.jboss.ejb.plugins.LogInterceptor] (WorkerThread#5[192.168.20.71:10806])  TransactionRolledbackException in method: public abstract javax.ejb.EJBObject javax.ejb.Handle.getEJBObject() throws java.rmi.RemoteException, causedBy:: java.rmi.NoSuchObjectException: Could not activate; failed to restore state
        at org.jboss.ejb.plugins.AbstractInstanceCache.get(AbstractInstanceCache.java:134) [:6.1.0.Final]
        at org.jboss.ejb.StatefulSessionContainer.getEJBObject(StatefulSessionContainer.java:394) [:6.1.0.Final]
        at sun.reflect.GeneratedMethodAccessor3683.invoke(Unknown Source) [:1.6.0_33]
        at sun.reflect.DelegatingMethodAccessorImpl.invoke(DelegatingMethodAccessorImpl.java:25) [:1.6.0_33]
        at java.lang.reflect.Method.invoke(Method.java:597) [:1.6.0_33]
        at org.jboss.invocation.Invocation.performCall(Invocation.java:386) [:6.1.0.Final]
        at org.jboss.ejb.StatefulSessionContainer$ContainerInterceptor.invokeHome(StatefulSessionContainer.java:564) [:6.1.0.Final]
        at org.jboss.ejb.plugins.StatefulSessionSecurityInterceptor.invokeHome(StatefulSessionSecurityInterceptor.java:97) [:6.1.0.Final]
        at org.jboss.ejb.plugins.SecurityInterceptor.process(SecurityInterceptor.java:270) [:6.1.0.Final]
        at org.jboss.ejb.plugins.SecurityInterceptor.invokeHome(SecurityInterceptor.java:205) [:6.1.0.Final]
        at org.jboss.resource.connectionmanager.CachedConnectionInterceptor.invokeHome(CachedConnectionInterceptor.java:178) [:6.1.0.Final]
        at org.jboss.ejb.plugins.StatefulSessionInstanceInterceptor.invokeHome(StatefulSessionInstanceInterceptor.java:127) [:6.1.0.Final]
        at org.jboss.ejb.plugins.CallValidationInterceptor.invokeHome(CallValidationInterceptor.java:56) [:6.1.0.Final]
        at org.jboss.ejb.plugins.AbstractTxInterceptor.invokeNext(AbstractTxInterceptor.java:125) [:6.1.0.Final]
        at org.jboss.ejb.plugins.TxInterceptorCMT.runWithTransactions(TxInterceptorCMT.java:350) [:6.1.0.Final]
        at org.jboss.ejb.plugins.TxInterceptorCMT.invokeHome(TxInterceptorCMT.java:161) [:6.1.0.Final]
        at org.jboss.ejb.plugins.security.PreSecurityInterceptor.process(PreSecurityInterceptor.java:160) [:6.1.0.Final]
        at org.jboss.ejb.plugins.security.PreSecurityInterceptor.invokeHome(PreSecurityInterceptor.java:91) [:6.1.0.Final]
        at org.jboss.ejb.plugins.LogInterceptor.invokeHome(LogInterceptor.java:132) [:6.1.0.Final]
        at org.jboss.ejb.plugins.ProxyFactoryFinderInterceptor.invokeHome(ProxyFactoryFinderInterceptor.java:107) [:6.1.0.Final]
        at org.jboss.ejb.SessionContainer.internalInvokeHome(SessionContainer.java:639) [:6.1.0.Final]
        at org.jboss.ejb.Container.invoke(Container.java:1089) [:6.1.0.Final]
        at sun.reflect.GeneratedMethodAccessor3461.invoke(Unknown Source) [:1.6.0_33]
        at sun.reflect.DelegatingMethodAccessorImpl.invoke(DelegatingMethodAccessorImpl.java:25) [:1.6.0_33]
        at java.lang.reflect.Method.invoke(Method.java:597) [:1.6.0_33]
        at org.jboss.mx.interceptor.ReflectedDispatcher.invoke(ReflectedDispatcher.java:157) [:6.0.0.GA]
        at org.jboss.mx.server.Invocation.dispatch(Invocation.java:96) [:6.0.0.GA]
        at org.jboss.mx.server.Invocation.invoke(Invocation.java:88) [:6.0.0.GA]
        at org.jboss.mx.server.AbstractMBeanInvoker.invoke(AbstractMBeanInvoker.java:271) [:6.0.0.GA]
        at org.jboss.mx.server.MBeanServerImpl.invoke(MBeanServerImpl.java:670) [:6.0.0.GA]
        at org.jboss.invocation.local.LocalInvoker$MBeanServerAction.invoke(LocalInvoker.java:169) [:6.1.0.Final]
        at org.jboss.invocation.local.LocalInvoker.invoke(LocalInvoker.java:118) [:6.1.0.Final]
        at org.jboss.invocation.InvokerInterceptor.invokeLocal(InvokerInterceptor.java:209) [:6.1.0.Final]
        at org.jboss.invocation.InvokerInterceptor.invoke(InvokerInterceptor.java:195) [:6.1.0.Final]
        at org.jboss.proxy.TransactionInterceptor.invoke(TransactionInterceptor.java:61) [:6.1.0.Final]
        at org.jboss.proxy.ejb.SecurityContextInterceptor.invoke(SecurityContextInterceptor.java:64) [:6.1.0.Final]
        at org.jboss.proxy.SecurityInterceptor.invoke(SecurityInterceptor.java:68) [:6.1.0.Final]
        at org.jboss.proxy.ejb.HomeInterceptor.invoke(HomeInterceptor.java:184) [:6.1.0.Final]
        at org.jboss.proxy.ClientContainer.invoke(ClientContainer.java:101) [:6.1.0.Final]
        at org.jboss.proxy.ejb.handle.StatefulHandleImpl.getEjbObjectViaJndi(StatefulHandleImpl.java:255) [:6.1.0.Final]
        at org.jboss.proxy.ejb.handle.StatefulHandleImpl.getEJBObject(StatefulHandleImpl.java:189) [:6.1.0.Final]
        at com.navahonetworks.ejb.session.app.LoginUserLogicBean.getLoginUserSF(LoginUserLogicBean.java:151) [:]
        at com.navahonetworks.ejb.session.app.LoginUserLogicBean.setUserContext(LoginUserLogicBean.java:891) [:]
        at sun.reflect.GeneratedMethodAccessor3877.invoke(Unknown Source) [:1.6.0_33]
        at sun.reflect.DelegatingMethodAccessorImpl.invoke(DelegatingMethodAccessorImpl.java:25) [:1.6.0_33]
        at java.lang.reflect.Method.invoke(Method.java:597) [:1.6.0_33]
        at org.jboss.invocation.Invocation.performCall(Invocation.java:386) [:6.1.0.Final]
        at org.jboss.ejb.StatelessSessionContainer$ContainerInterceptor.invoke(StatelessSessionContainer.java:233) [:6.1.0.Final]
        at org.jboss.resource.connectionmanager.CachedConnectionInterceptor.invoke(CachedConnectionInterceptor.java:156) [:6.1.0.Final]
        at org.jboss.ejb.plugins.StatelessSessionInstanceInterceptor.invoke(StatelessSessionInstanceInterceptor.java:173) [:6.1.0.Final]
        at org.jboss.ejb.plugins.CallValidationInterceptor.invoke(CallValidationInterceptor.java:63) [:6.1.0.Final]
        at org.jboss.ejb.plugins.AbstractTxInterceptor.invokeNext(AbstractTxInterceptor.java:121) [:6.1.0.Final]
        at org.jboss.ejb.plugins.TxInterceptorCMT.runWithTransactions(TxInterceptorCMT.java:350) [:6.1.0.Final]
        at org.jboss.ejb.plugins.TxInterceptorCMT.invoke(TxInterceptorCMT.java:181) [:6.1.0.Final]
        at org.jboss.ejb.plugins.SecurityInterceptor.process(SecurityInterceptor.java:268) [:6.1.0.Final]
        at org.jboss.ejb.plugins.SecurityInterceptor.invoke(SecurityInterceptor.java:211) [:6.1.0.Final]
        at org.jboss.ejb.plugins.security.PreSecurityInterceptor.process(PreSecurityInterceptor.java:158) [:6.1.0.Final]
        at org.jboss.ejb.plugins.security.PreSecurityInterceptor.invoke(PreSecurityInterceptor.java:84) [:6.1.0.Final]
        at org.jboss.ejb.plugins.LogInterceptor.invoke(LogInterceptor.java:205) [:6.1.0.Final]
        at org.jboss.ejb.plugins.ProxyFactoryFinderInterceptor.invoke(ProxyFactoryFinderInterceptor.java:138) [:6.1.0.Final]
        at org.jboss.ejb.SessionContainer.internalInvoke(SessionContainer.java:650) [:6.1.0.Final]
        at org.jboss.ejb.Container.invoke(Container.java:1072) [:6.1.0.Final]
        at sun.reflect.GeneratedMethodAccessor3461.invoke(Unknown Source) [:1.6.0_33]
        at sun.reflect.DelegatingMethodAccessorImpl.invoke(DelegatingMethodAccessorImpl.java:25) [:1.6.0_33]
        at java.lang.reflect.Method.invoke(Method.java:597) [:1.6.0_33]
        at org.jboss.mx.interceptor.ReflectedDispatcher.invoke(ReflectedDispatcher.java:157) [:6.0.0.GA]
        at org.jboss.mx.server.Invocation.dispatch(Invocation.java:96) [:6.0.0.GA]
        at org.jboss.mx.server.Invocation.invoke(Invocation.java:88) [:6.0.0.GA]
        at org.jboss.mx.server.AbstractMBeanInvoker.invoke(AbstractMBeanInvoker.java:271) [:6.0.0.GA]
        at org.jboss.mx.server.MBeanServerImpl.invoke(MBeanServerImpl.java:670) [:6.0.0.GA]
        at org.jboss.invocation.unified.server.UnifiedInvoker.invoke(UnifiedInvoker.java:232) [:6.1.0.Final]
        at org.jboss.remoting.ServerInvoker.invoke(ServerInvoker.java:967) [:6.1.0.Final]
        at org.jboss.remoting.transport.socket.ServerThread.completeInvocation(ServerThread.java:791) [:6.1.0.Final]
        at org.jboss.remoting.transport.socket.ServerThread.processInvocation(ServerThread.java:744) [:6.1.0.Final]
        at org.jboss.remoting.transport.socket.ServerThread.dorun(ServerThread.java:548) [:6.1.0.Final]
        at org.jboss.remoting.transport.socket.ServerThread.run(ServerThread.java:234) [:6.1.0.Final]

2012-10-02 00:01:32,117 ERROR [com.navahonetworks.ejb.session.app.LoginUserLogicBean] (WorkerThread#5[192.168.20.71:10806])  couldn't get loginUserSF by handle: Could not activate; failed to restore state; nested exception is: 
        java.rmi.NoSuchObjectException: Could not activate; failed to restore state
2012-10-02 00:01:32,119 DEBUG [org.jboss.ejb.plugins.AbstractInstanceCache] (WorkerThread#5[192.168.20.71:10806])  Activation failure: javax.ejb.EJBException: Could not activate; failed to restore state
        at org.jboss.ejb.plugins.StatefulSessionFilePersistenceManager.activateSession(StatefulSessionFilePersistenceManager.java:343) [:6.1.0.Final]
        at org.jboss.ejb.plugins.StatefulSessionInstanceCache.activate(StatefulSessionInstanceCache.java:113) [:6.1.0.Final]
        at org.jboss.ejb.plugins.AbstractInstanceCache.doActivate(AbstractInstanceCache.java:458) [:6.1.0.Final]
        at org.jboss.ejb.plugins.StatefulSessionInstanceCache.doActivate(StatefulSessionInstanceCache.java:129) [:6.1.0.Final]
        at org.jboss.ejb.plugins.AbstractInstanceCache.get(AbstractInstanceCache.java:123) [:6.1.0.Final]
        at org.jboss.ejb.StatefulSessionContainer.getEJBObject(StatefulSessionContainer.java:394) [:6.1.0.Final]
        at sun.reflect.GeneratedMethodAccessor3683.invoke(Unknown Source) [:1.6.0_33]
        at sun.reflect.DelegatingMethodAccessorImpl.invoke(DelegatingMethodAccessorImpl.java:25) [:1.6.0_33]
        at java.lang.reflect.Method.invoke(Method.java:597) [:1.6.0_33]
        at org.jboss.invocation.Invocation.performCall(Invocation.java:386) [:6.1.0.Final]
        at org.jboss.ejb.StatefulSessionContainer$ContainerInterceptor.invokeHome(StatefulSessionContainer.java:564) [:6.1.0.Final]
        at org.jboss.ejb.plugins.StatefulSessionSecurityInterceptor.invokeHome(StatefulSessionSecurityInterceptor.java:97) [:6.1.0.Final]
        at org.jboss.ejb.plugins.SecurityInterceptor.process(SecurityInterceptor.java:270) [:6.1.0.Final]
        at org.jboss.ejb.plugins.SecurityInterceptor.invokeHome(SecurityInterceptor.java:205) [:6.1.0.Final]
        at org.jboss.resource.connectionmanager.CachedConnectionInterceptor.invokeHome(CachedConnectionInterceptor.java:178) [:6.1.0.Final]
        at org.jboss.ejb.plugins.StatefulSessionInstanceInterceptor.invokeHome(StatefulSessionInstanceInterceptor.java:127) [:6.1.0.Final]
        at org.jboss.ejb.plugins.CallValidationInterceptor.invokeHome(CallValidationInterceptor.java:56) [:6.1.0.Final]
        at org.jboss.ejb.plugins.AbstractTxInterceptor.invokeNext(AbstractTxInterceptor.java:125) [:6.1.0.Final]
        at org.jboss.ejb.plugins.TxInterceptorCMT.runWithTransactions(TxInterceptorCMT.java:350) [:6.1.0.Final]
        at org.jboss.ejb.plugins.TxInterceptorCMT.invokeHome(TxInterceptorCMT.java:161) [:6.1.0.Final]
        at org.jboss.ejb.plugins.security.PreSecurityInterceptor.process(PreSecurityInterceptor.java:160) [:6.1.0.Final]
        at org.jboss.ejb.plugins.security.PreSecurityInterceptor.invokeHome(PreSecurityInterceptor.java:91) [:6.1.0.Final]
        at org.jboss.ejb.plugins.LogInterceptor.invokeHome(LogInterceptor.java:132) [:6.1.0.Final]
        at org.jboss.ejb.plugins.ProxyFactoryFinderInterceptor.invokeHome(ProxyFactoryFinderInterceptor.java:107) [:6.1.0.Final]
        at org.jboss.ejb.SessionContainer.internalInvokeHome(SessionContainer.java:639) [:6.1.0.Final]
        at org.jboss.ejb.Container.invoke(Container.java:1089) [:6.1.0.Final]
        at sun.reflect.GeneratedMethodAccessor3461.invoke(Unknown Source) [:1.6.0_33]
        at sun.reflect.DelegatingMethodAccessorImpl.invoke(DelegatingMethodAccessorImpl.java:25) [:1.6.0_33]
        at java.lang.reflect.Method.invoke(Method.java:597) [:1.6.0_33]
        at org.jboss.mx.interceptor.ReflectedDispatcher.invoke(ReflectedDispatcher.java:157) [:6.0.0.GA]
        at org.jboss.mx.server.Invocation.dispatch(Invocation.java:96) [:6.0.0.GA]
        at org.jboss.mx.server.Invocation.invoke(Invocation.java:88) [:6.0.0.GA]
        at org.jboss.mx.server.AbstractMBeanInvoker.invoke(AbstractMBeanInvoker.java:271) [:6.0.0.GA]
        at org.jboss.mx.server.MBeanServerImpl.invoke(MBeanServerImpl.java:670) [:6.0.0.GA]
        at org.jboss.invocation.local.LocalInvoker$MBeanServerAction.invoke(LocalInvoker.java:169) [:6.1.0.Final]
        at org.jboss.invocation.local.LocalInvoker.invoke(LocalInvoker.java:118) [:6.1.0.Final]
        at org.jboss.invocation.InvokerInterceptor.invokeLocal(InvokerInterceptor.java:209) [:6.1.0.Final]
        at org.jboss.invocation.InvokerInterceptor.invoke(InvokerInterceptor.java:195) [:6.1.0.Final]
        at org.jboss.proxy.TransactionInterceptor.invoke(TransactionInterceptor.java:61) [:6.1.0.Final]
        at org.jboss.proxy.ejb.SecurityContextInterceptor.invoke(SecurityContextInterceptor.java:64) [:6.1.0.Final]
        at org.jboss.proxy.SecurityInterceptor.invoke(SecurityInterceptor.java:68) [:6.1.0.Final]
        at org.jboss.proxy.ejb.HomeInterceptor.invoke(HomeInterceptor.java:184) [:6.1.0.Final]
        at org.jboss.proxy.ClientContainer.invoke(ClientContainer.java:101) [:6.1.0.Final]
        at org.jboss.proxy.ejb.handle.StatefulHandleImpl.getEjbObjectViaJndi(StatefulHandleImpl.java:255) [:6.1.0.Final]
        at org.jboss.proxy.ejb.handle.StatefulHandleImpl.getEJBObject(StatefulHandleImpl.java:189) [:6.1.0.Final]
        at com.navahonetworks.ejb.session.NNAbstractSession.getLoginUserLocal(NNAbstractSession.java:72) [:]
        at com.navahonetworks.ejb.session.app.LoginUserLogicBean.isLoginUserHandleAvailable(LoginUserLogicBean.java:195) [:]
        at sun.reflect.GeneratedMethodAccessor3789.invoke(Unknown Source) [:1.6.0_33]
        at sun.reflect.DelegatingMethodAccessorImpl.invoke(DelegatingMethodAccessorImpl.java:25) [:1.6.0_33]
        at java.lang.reflect.Method.invoke(Method.java:597) [:1.6.0_33]
        at org.jboss.invocation.Invocation.performCall(Invocation.java:386) [:6.1.0.Final]
        at org.jboss.ejb.StatelessSessionContainer$ContainerInterceptor.invoke(StatelessSessionContainer.java:233) [:6.1.0.Final]
        at org.jboss.resource.connectionmanager.CachedConnectionInterceptor.invoke(CachedConnectionInterceptor.java:156) [:6.1.0.Final]
        at org.jboss.ejb.plugins.StatelessSessionInstanceInterceptor.invoke(StatelessSessionInstanceInterceptor.java:173) [:6.1.0.Final]
        at org.jboss.ejb.plugins.CallValidationInterceptor.invoke(CallValidationInterceptor.java:63) [:6.1.0.Final]
        at org.jboss.ejb.plugins.AbstractTxInterceptor.invokeNext(AbstractTxInterceptor.java:121) [:6.1.0.Final]
        at org.jboss.ejb.plugins.TxInterceptorCMT.runWithTransactions(TxInterceptorCMT.java:350) [:6.1.0.Final]
        at org.jboss.ejb.plugins.TxInterceptorCMT.invoke(TxInterceptorCMT.java:181) [:6.1.0.Final]
        at org.jboss.ejb.plugins.SecurityInterceptor.process(SecurityInterceptor.java:268) [:6.1.0.Final]
        at org.jboss.ejb.plugins.SecurityInterceptor.invoke(SecurityInterceptor.java:211) [:6.1.0.Final]
        at org.jboss.ejb.plugins.security.PreSecurityInterceptor.process(PreSecurityInterceptor.java:158) [:6.1.0.Final]
        at org.jboss.ejb.plugins.security.PreSecurityInterceptor.invoke(PreSecurityInterceptor.java:84) [:6.1.0.Final]
        at org.jboss.ejb.plugins.LogInterceptor.invoke(LogInterceptor.java:205) [:6.1.0.Final]
        at org.jboss.ejb.plugins.ProxyFactoryFinderInterceptor.invoke(ProxyFactoryFinderInterceptor.java:138) [:6.1.0.Final]
        at org.jboss.ejb.SessionContainer.internalInvoke(SessionContainer.java:650) [:6.1.0.Final]
        at org.jboss.ejb.Container.invoke(Container.java:1072) [:6.1.0.Final]
        at sun.reflect.GeneratedMethodAccessor3461.invoke(Unknown Source) [:1.6.0_33]
        at sun.reflect.DelegatingMethodAccessorImpl.invoke(DelegatingMethodAccessorImpl.java:25) [:1.6.0_33]
        at java.lang.reflect.Method.invoke(Method.java:597) [:1.6.0_33]
        at org.jboss.mx.interceptor.ReflectedDispatcher.invoke(ReflectedDispatcher.java:157) [:6.0.0.GA]
        at org.jboss.mx.server.Invocation.dispatch(Invocation.java:96) [:6.0.0.GA]
        at org.jboss.mx.server.Invocation.invoke(Invocation.java:88) [:6.0.0.GA]
        at org.jboss.mx.server.AbstractMBeanInvoker.invoke(AbstractMBeanInvoker.java:271) [:6.0.0.GA]
        at org.jboss.mx.server.MBeanServerImpl.invoke(MBeanServerImpl.java:670) [:6.0.0.GA]
        at org.jboss.invocation.unified.server.UnifiedInvoker.invoke(UnifiedInvoker.java:232) [:6.1.0.Final]
        at org.jboss.remoting.ServerInvoker.invoke(ServerInvoker.java:967) [:6.1.0.Final]
        at org.jboss.remoting.transport.socket.ServerThread.completeInvocation(ServerThread.java:791) [:6.1.0.Final]
        at org.jboss.remoting.transport.socket.ServerThread.processInvocation(ServerThread.java:744) [:6.1.0.Final]
        at org.jboss.remoting.transport.socket.ServerThread.dorun(ServerThread.java:586) [:6.1.0.Final]
        at org.jboss.remoting.transport.socket.ServerThread.run(ServerThread.java:234) [:6.1.0.Final]
Caused by: java.io.FileNotFoundException: /usr/local/java/jboss-6.1.0.Final/server/prod.ejb/tmp/sessions/LoginUserSF-h7rxw4f1-p6/h7s6anht-pg.ser (No such file or directory)
        at java.io.FileInputStream.open(Native Method) [:1.6.0_33]
        at java.io.FileInputStream.<init>(FileInputStream.java:120) [:1.6.0_33]
        at org.jboss.ejb.plugins.StatefulSessionFilePersistenceManager$FISAction.run(StatefulSessionFilePersistenceManager.java:526) [:6.1.0.Final]
        at java.security.AccessController.doPrivileged(Native Method) [:1.6.0_33]
        at org.jboss.ejb.plugins.StatefulSessionFilePersistenceManager$FISAction.open(StatefulSessionFilePersistenceManager.java:535) [:6.1.0.Final]
        at org.jboss.ejb.plugins.StatefulSessionFilePersistenceManager.activateSession(StatefulSessionFilePersistenceManager.java:323) [:6.1.0.Final]
        ... 79 more

2012-10-02 01:20:00,008 DEBUG [com.riavera.ejb.session.EventDispatcherBean] (DefaultQuartzScheduler_Worker-7)  getting pending events
2012-10-02 01:20:00,009 DEBUG [org.hibernate.impl.SessionImpl] (DefaultQuartzScheduler_Worker-7)  opened session at timestamp: 5526080716836864
2012-10-02 01:20:00,009 DEBUG [org.hibernate.ejb.AbstractEntityManagerImpl] (DefaultQuartzScheduler_Worker-7)  Looking for a JTA transaction to join
2012-10-02 01:20:00,009 DEBUG [org.hibernate.jdbc.JDBCContext] (DefaultQuartzScheduler_Worker-7)  successfully registered Synchronization
2012-10-02 01:20:00,009 DEBUG [org.hibernate.ejb.AbstractEntityManagerImpl] (DefaultQuartzScheduler_Worker-7)  Looking for a JTA transaction to join
2012-10-02 01:20:00,009 DEBUG [org.hibernate.ejb.AbstractEntityManagerImpl] (DefaultQuartzScheduler_Worker-7)  Transaction already joined
2012-10-02 01:20:00,009 DEBUG [org.hibernate.jdbc.AbstractBatcher] (DefaultQuartzScheduler_Worker-7)  about to open PreparedStatement (open PreparedStatements: 0, globally: 0)
2012-10-02 01:20:00,009 DEBUG [org.hibernate.jdbc.ConnectionManager] (DefaultQuartzScheduler_Worker-7)  opening JDBC connection
2012-10-02 01:20:00,010 DEBUG [org.hibernate.SQL] (DefaultQuartzScheduler_Worker-7)  select * from ( SELECT * FROM offnet.event WHERE ((state IN ('P','B') AND next_attempt <= SYSTIMESTAMP) OR (state='C' AND parent_event_guid IS NULL)) AND (locked_by IS NULL OR locked_by = ?) CONNECT BY PRIOR event_guid=parent_event_guid ) where rownum <= ?
2012-10-02 01:20:00,010 DEBUG [org.hibernate.loader.Loader] (DefaultQuartzScheduler_Worker-7)  bindNamedParameters() thor.prod.tor.riavera.com -> procId [1]
2012-10-02 01:20:00,012 DEBUG [org.hibernate.jdbc.AbstractBatcher] (DefaultQuartzScheduler_Worker-7)  about to open ResultSet (open ResultSets: 0, globally: 0)
2012-10-02 01:20:00,012 DEBUG [org.hibernate.jdbc.AbstractBatcher] (DefaultQuartzScheduler_Worker-7)  about to close ResultSet (open ResultSets: 1, globally: 1)
2012-10-02 01:20:00,012 DEBUG [org.hibernate.jdbc.AbstractBatcher] (DefaultQuartzScheduler_Worker-7)  about to close PreparedStatement (open PreparedStatements: 1, globally: 1)
2012-10-02 01:20:00,012 DEBUG [org.hibernate.jdbc.ConnectionManager] (DefaultQuartzScheduler_Worker-7)  aggressively releasing JDBC connection
2012-10-02 01:20:00,012 DEBUG [org.hibernate.jdbc.ConnectionManager] (DefaultQuartzScheduler_Worker-7)  releasing JDBC connection [ (open PreparedStatements: 0, globally: 0) (open ResultSets: 0, globally: 0)]
2012-10-02 01:20:00,012 DEBUG [org.hibernate.engine.StatefulPersistenceContext] (DefaultQuartzScheduler_Worker-7)  initializing non-lazy collections
2012-10-02 01:20:00,012 INFO  [com.riavera.ejb.session.EventDispatcherBean] (DefaultQuartzScheduler_Worker-7)  found 0 events to process
2012-10-02 01:20:00,012 DEBUG [org.jboss.jpa.deployment.ManagedEntityManagerFactory] (DefaultQuartzScheduler_Worker-7)  ************** closing entity managersession **************
2012-10-02 01:20:07,363 DEBUG [org.jboss.modcluster.ModClusterService] (ContainerBackgroundProcessor[StandardEngine[jboss.web]])  Check status for engine [jboss.web]
2012-10-02 01:20:17,364 DEBUG [org.jboss.modcluster.ModClusterService] (ContainerBackgroundProcessor[StandardEngine[jboss.web]])  Check status for engine [jboss.web]
2012-10-02 01:20:19,572 DEBUG [org.jboss.remoting.transport.socket.ServerThread] (WorkerThread#0[192.168.20.71:42714])  WorkerThread#0[192.168.20.71:42714] closed socketWrapper: ServerSocketWrapper[Socket[addr=/192.168.20.71,port=42714,localport=4446].40dfa112]
2012-10-02 01:20:27,364 DEBUG [org.jboss.modcluster.ModClusterService] (ContainerBackgroundProcessor[StandardEngine[jboss.web]])  Check status for engine [jboss.web]
2012-10-02 01:20:37,364 DEBUG [org.jboss.modcluster.ModClusterService] (ContainerBackgroundProcessor[StandardEngine[jboss.web]])  Check status for engine [jboss.web]
2012-10-02 01:20:43,915 DEBUG [org.jboss.ejb.plugins.LRUEnterpriseContextCachePolicy] (Timer-1)  Running RemoverTask
2012-10-02 01:20:43,916 DEBUG [org.jboss.ejb.plugins.LRUEnterpriseContextCachePolicy] (Timer-1)  RemoverTask, PassivatedCount=0
2012-10-02 01:20:43,916 DEBUG [org.jboss.ejb.plugins.AbstractInstanceCache] (Timer-1)  removePassivated, now=1349140843916, maxLifeAfterPassivation=1200000
2012-10-02 01:20:43,916 DEBUG [org.jboss.ejb.plugins.LRUEnterpriseContextCachePolicy] (Timer-1)  RemoverTask, done
2012-10-02 01:20:47,365 DEBUG [org.jboss.modcluster.ModClusterService] (ContainerBackgroundProcessor[StandardEngine[jboss.web]])  Check status for engine [jboss.web]
2012-10-02 01:20:57,365 DEBUG [org.jboss.modcluster.ModClusterService] (ContainerBackgroundProcessor[StandardEngine[jboss.web]])  Check status for engine [jboss.web]
2012-10-02 01:21:07,365 DEBUG [org.jboss.modcluster.ModClusterService] (ContainerBackgroundProcessor[StandardEngine[jboss.web]])  Check status for engine [jboss.web]
2012-10-02 01:21:17,366 DEBUG [org.jboss.modcluster.ModClusterService] (ContainerBackgroundProcessor[StandardEngine[jboss.web]])  Check status for engine [jboss.web]
2012-10-02 01:21:27,366 DEBUG [org.jboss.modcluster.ModClusterService] (ContainerBackgroundProcessor[StandardEngine[jboss.web]])  Check status for engine [jboss.web]
2012-10-02 01:21:37,366 DEBUG [org.jboss.modcluster.ModClusterService] (ContainerBackgroundProcessor[StandardEngine[jboss.web]])  Check status for engine [jboss.web]
2012-10-02 01:21:43,915 DEBUG [org.jboss.ejb.plugins.LRUEnterpriseContextCachePolicy] (Timer-1)  Running RemoverTask
2012-10-02 01:21:43,915 DEBUG [org.jboss.ejb.plugins.LRUEnterpriseContextCachePolicy] (Timer-1)  RemoverTask, PassivatedCount=0
2012-10-02 01:21:43,915 DEBUG [org.jboss.ejb.plugins.AbstractInstanceCache] (Timer-1)  removePassivated, now=1349140903915, maxLifeAfterPassivation=1200000
2012-10-02 01:21:43,915 DEBUG [org.jboss.ejb.plugins.LRUEnterpriseContextCachePolicy] (Timer-1)  RemoverTask, done
2012-10-02 01:21:47,366 DEBUG [org.jboss.modcluster.ModClusterService] (ContainerBackgroundProcessor[StandardEngine[jboss.web]])  Check status for engine [jboss.web]
2012-10-02 01:21:57,367 DEBUG [org.jboss.modcluster.ModClusterService] (ContainerBackgroundProcessor[StandardEngine[jboss.web]])  Check status for engine [jboss.web]
2012-10-02 01:22:04,545 DEBUG [org.jboss.remoting.transport.socket.ServerThread] (WorkerThread#2[192.168.20.71:10197])  WorkerThread#2[192.168.20.71:10197] closed socketWrapper: ServerSocketWrapper[Socket[addr=/192.168.20.71,port=10197,localport=3873].28e28e84]
2012-10-02 01:22:04,547 DEBUG [org.jboss.ejb3.stateless.StatelessContainer] (WorkerThread#1[192.168.20.71:10198])  Received dynamic invocation for method with hash: -1707116595046585177
2012-10-02 01:22:04,553 DEBUG [com.riavera.ejb.session.GeoBean] (WorkerThread#1[192.168.20.71:10198])  ipToCountry lookup for ip 72.14.199.102 with provider null
2012-10-02 01:22:04,553 DEBUG [org.jboss.ejb3.common.registrar.plugin.mc.Ejb3McRegistrar] (WorkerThread#1[192.168.20.71:10198])  Returning from name "jboss.j2ee:ear=wallet-core.ear,jar=ejb.jar,name=ConfigBean,service=EJB3": jboss.j2ee:ear=wallet-core.ear,jar=ejb.jar,name=ConfigBean,service=EJB3
2012-10-02 01:22:04,556 DEBUG [org.hibernate.jdbc.AbstractBatcher] (WorkerThread#1[192.168.20.71:10198])  about to close ResultSet (open ResultSets: 1, globally: 1)
2012-10-02 01:22:04,556 DEBUG [org.hibernate.jdbc.AbstractBatcher] (WorkerThread#1[192.168.20.71:10198])  about to close PreparedStatement (open PreparedStatements: 1, globally: 1)
2012-10-02 01:22:04,556 DEBUG [org.hibernate.jdbc.ConnectionManager] (WorkerThread#1[192.168.20.71:10198])  aggressively releasing JDBC connection
2012-10-02 01:22:04,556 DEBUG [org.hibernate.jdbc.ConnectionManager] (WorkerThread#1[192.168.20.71:10198])  releasing JDBC connection [ (open PreparedStatements: 0, globally: 0) (open ResultSets: 0, globally: 0)]
2012-10-02 01:22:04,556 DEBUG [org.hibernate.engine.TwoPhaseLoad] (WorkerThread#1[192.168.20.71:10198])  resolving associations for [com.riavera.ejb.entity.ServiceConfig#component[parameter,service]{parameter=default_geoip_provider, service=default}]
2012-10-02 01:22:04,556 DEBUG [org.hibernate.engine.TwoPhaseLoad] (WorkerThread#1[192.168.20.71:10198])  done materializing entity [com.riavera.ejb.entity.ServiceConfig#component[parameter,service]{parameter=default_geoip_provider, service=default}]
2012-10-02 01:22:04,556 DEBUG [org.hibernate.engine.StatefulPersistenceContext] (WorkerThread#1[192.168.20.71:10198])  initializing non-lazy collections
2012-10-02 01:22:04,557 DEBUG [org.hibernate.event.def.AbstractFlushingEventListener] (WorkerThread#1[192.168.20.71:10198])  processing flush-time cascades
2012-10-02 01:22:04,557 DEBUG [org.hibernate.event.def.AbstractFlushingEventListener] (WorkerThread#1[192.168.20.71:10198])  dirty checking collections
2012-10-02 01:22:04,557 DEBUG [org.hibernate.event.def.AbstractFlushingEventListener] (WorkerThread#1[192.168.20.71:10198])  Flushed: 0 insertions, 0 updates, 0 deletions to 1 objects
2012-10-02 01:22:04,557 DEBUG [org.hibernate.event.def.AbstractFlushingEventListener] (WorkerThread#1[192.168.20.71:10198])  Flushed: 0 (re)creations, 0 updates, 0 removals to 0 collections
2012-10-02 01:22:04,557 DEBUG [org.hibernate.pretty.Printer] (WorkerThread#1[192.168.20.71:10198])  listing entities:
2012-10-02 01:22:04,557 DEBUG [org.hibernate.pretty.Printer] (WorkerThread#1[192.168.20.71:10198])  com.riavera.ejb.entity.ServiceConfig{parameter=default_geoip_provider, value=ip-to-country, service=default, version=0, pk=component[parameter,service]{parameter=default_geoip_provider, service=default}}
2012-10-02 01:22:04,557 DEBUG [org.hibernate.jdbc.AbstractBatcher] (WorkerThread#1[192.168.20.71:10198])  about to open PreparedStatement (open PreparedStatements: 0, globally: 0)
2012-10-02 01:22:04,557 DEBUG [org.hibernate.jdbc.ConnectionManager] (WorkerThread#1[192.168.20.71:10198])  opening JDBC connection
2012-10-02 01:22:04,557 DEBUG [org.hibernate.SQL] (WorkerThread#1[192.168.20.71:10198])  select geoipprovi0_.GEO_IP_PROVIDER_GUID as GEO1_124_, geoipprovi0_.DESCRIPTION as DESCRIPT2_124_, geoipprovi0_.NAME as NAME124_ from offnet.GEO_IP_PROVIDER geoipprovi0_ where geoipprovi0_.NAME=?
2012-10-02 01:22:04,557 DEBUG [org.hibernate.jdbc.AbstractBatcher] (WorkerThread#1[192.168.20.71:10198])  about to open ResultSet (open ResultSets: 0, globally: 0)
2012-10-02 01:22:04,557 DEBUG [org.hibernate.loader.Loader] (WorkerThread#1[192.168.20.71:10198])  result row: EntityKey[com.riavera.ejb.entity.GeoIpProvider#BA4664A3A206806DE040A8C082143384]
2012-10-02 01:22:04,558 DEBUG [org.hibernate.jdbc.AbstractBatcher] (WorkerThread#1[192.168.20.71:10198])  about to close ResultSet (open ResultSets: 1, globally: 1)
2012-10-02 01:22:04,558 DEBUG [org.hibernate.jdbc.AbstractBatcher] (WorkerThread#1[192.168.20.71:10198])  about to close PreparedStatement (open PreparedStatements: 1, globally: 1)
2012-10-02 01:22:04,558 DEBUG [org.hibernate.jdbc.ConnectionManager] (WorkerThread#1[192.168.20.71:10198])  aggressively releasing JDBC connection
2012-10-02 01:22:04,558 DEBUG [org.hibernate.jdbc.ConnectionManager] (WorkerThread#1[192.168.20.71:10198])  releasing JDBC connection [ (open PreparedStatements: 0, globally: 0) (open ResultSets: 0, globally: 0)]
2012-10-02 01:22:04,558 DEBUG [org.hibernate.engine.TwoPhaseLoad] (WorkerThread#1[192.168.20.71:10198])  resolving associations for [com.riavera.ejb.entity.GeoIpProvider#BA4664A3A206806DE040A8C082143384]
2012-10-02 01:22:04,558 DEBUG [org.hibernate.engine.TwoPhaseLoad] (WorkerThread#1[192.168.20.71:10198])  done materializing entity [com.riavera.ejb.entity.GeoIpProvider#BA4664A3A206806DE040A8C082143384]
2012-10-02 01:22:04,558 DEBUG [org.hibernate.engine.StatefulPersistenceContext] (WorkerThread#1[192.168.20.71:10198])  initializing non-lazy collections
2012-10-02 01:22:04,558 DEBUG [com.riavera.ejb.session.GeoBean] (WorkerThread#1[192.168.20.71:10198])  using IP to country provider: ip-to-country
2012-10-02 01:22:04,558 DEBUG [com.riavera.ejb.session.GeoBean] (WorkerThread#1[192.168.20.71:10198])  searching for country for ip=72.14.199.102, dec=1208928102
2012-10-02 01:22:04,558 DEBUG [org.hibernate.event.def.AbstractFlushingEventListener] (WorkerThread#1[192.168.20.71:10198])  processing flush-time cascades
2012-10-02 01:22:04,558 DEBUG [org.hibernate.event.def.AbstractFlushingEventListener] (WorkerThread#1[192.168.20.71:10198])  dirty checking collections
2012-10-02 01:22:04,558 DEBUG [org.hibernate.event.def.AbstractFlushingEventListener] (WorkerThread#1[192.168.20.71:10198])  Flushed: 0 insertions, 0 updates, 0 deletions to 2 objects
2012-10-02 01:22:04,558 DEBUG [org.hibernate.event.def.AbstractFlushingEventListener] (WorkerThread#1[192.168.20.71:10198])  Flushed: 0 (re)creations, 0 updates, 0 removals to 0 collections
2012-10-02 01:22:04,558 DEBUG [org.hibernate.pretty.Printer] (WorkerThread#1[192.168.20.71:10198])  listing entities:
2012-10-02 01:22:04,558 DEBUG [org.hibernate.pretty.Printer] (WorkerThread#1[192.168.20.71:10198])  com.riavera.ejb.entity.ServiceConfig{parameter=default_geoip_provider, value=ip-to-country, service=default, version=0, pk=component[parameter,service]{parameter=default_geoip_provider, service=default}}
2012-10-02 01:22:04,558 DEBUG [org.hibernate.pretty.Printer] (WorkerThread#1[192.168.20.71:10198])  com.riavera.ejb.entity.GeoIpProvider{description=http://www.ip-to-country.com/, name=ip-to-country, geoIpProviderGuid=BA4664A3A206806DE040A8C082143384}
2012-10-02 01:22:04,558 DEBUG [org.hibernate.jdbc.AbstractBatcher] (WorkerThread#1[192.168.20.71:10198])  about to open PreparedStatement (open PreparedStatements: 0, globally: 0)
2012-10-02 01:22:04,558 DEBUG [org.hibernate.jdbc.ConnectionManager] (WorkerThread#1[192.168.20.71:10198])  opening JDBC connection
2012-10-02 01:22:04,558 DEBUG [org.hibernate.SQL] (WorkerThread#1[192.168.20.71:10198])  select geoipdata0_.GEO_IP_PROVIDER_GUID as GEO1_123_, geoipdata0_.IP_FROM as IP2_123_, geoipdata0_.IP_TO as IP3_123_, geoipdata0_.CITY as CITY123_, geoipdata0_.COUNTRY as COUNTRY123_, geoipdata0_.ENTRY_DATE as ENTRY6_123_, geoipdata0_.PROVINCE as PROVINCE123_ from offnet.GEO_IP_DATA geoipdata0_ where geoipdata0_.GEO_IP_PROVIDER_GUID=? and geoipdata0_.IP_FROM<=? and geoipdata0_.IP_TO>=?
2012-10-02 01:22:04,574 DEBUG [org.hibernate.jdbc.AbstractBatcher] (WorkerThread#1[192.168.20.71:10198])  about to open ResultSet (open ResultSets: 0, globally: 0)
2012-10-02 01:22:04,574 DEBUG [org.hibernate.loader.Loader] (WorkerThread#1[192.168.20.71:10198])  result row: EntityKey[com.riavera.ejb.entity.GeoIpData#component[geoIpProviderGuid,ipFrom,ipTo]{ipTo=1208954879, ipFrom=1208922112, geoIpProviderGuid=BA4664A3A206806DE040A8C082143384}]
2012-10-02 01:22:04,575 DEBUG [org.hibernate.jdbc.AbstractBatcher] (WorkerThread#1[192.168.20.71:10198])  about to close ResultSet (open ResultSets: 1, globally: 1)
2012-10-02 01:22:04,575 DEBUG [org.hibernate.jdbc.AbstractBatcher] (WorkerThread#1[192.168.20.71:10198])  about to close PreparedStatement (open PreparedStatements: 1, globally: 1)
2012-10-02 01:22:04,575 DEBUG [org.hibernate.jdbc.ConnectionManager] (WorkerThread#1[192.168.20.71:10198])  aggressively releasing JDBC connection
2012-10-02 01:22:04,575 DEBUG [org.hibernate.jdbc.ConnectionManager] (WorkerThread#1[192.168.20.71:10198])  releasing JDBC connection [ (open PreparedStatements: 0, globally: 0) (open ResultSets: 0, globally: 0)]
2012-10-02 01:22:04,575 DEBUG [org.hibernate.engine.TwoPhaseLoad] (WorkerThread#1[192.168.20.71:10198])  resolving associations for [com.riavera.ejb.entity.GeoIpData#component[geoIpProviderGuid,ipFrom,ipTo]{ipTo=1208954879, ipFrom=1208922112, geoIpProviderGuid=BA4664A3A206806DE040A8C082143384}]
2012-10-02 01:22:04,575 DEBUG [org.hibernate.engine.TwoPhaseLoad] (WorkerThread#1[192.168.20.71:10198])  done materializing entity [com.riavera.ejb.entity.GeoIpData#component[geoIpProviderGuid,ipFrom,ipTo]{ipTo=1208954879, ipFrom=1208922112, geoIpProviderGuid=BA4664A3A206806DE040A8C082143384}]
2012-10-02 01:22:04,575 DEBUG [org.hibernate.engine.StatefulPersistenceContext] (WorkerThread#1[192.168.20.71:10198])  initializing non-lazy collections
2012-10-02 01:22:04,575 INFO  [com.riavera.ejb.session.GeoBean] (WorkerThread#1[192.168.20.71:10198])  found country US for ip 72.14.199.102
2012-10-02 01:22:04,575 DEBUG [org.hibernate.event.def.AbstractFlushingEventListener] (WorkerThread#1[192.168.20.71:10198])  processing flush-time cascades
2012-10-02 01:22:04,575 DEBUG [org.hibernate.event.def.AbstractFlushingEventListener] (WorkerThread#1[192.168.20.71:10198])  dirty checking collections
2012-10-02 01:22:04,575 DEBUG [org.hibernate.event.def.AbstractFlushingEventListener] (WorkerThread#1[192.168.20.71:10198])  Flushed: 0 insertions, 0 updates, 0 deletions to 3 objects
2012-10-02 01:22:04,575 DEBUG [org.hibernate.event.def.AbstractFlushingEventListener] (WorkerThread#1[192.168.20.71:10198])  Flushed: 0 (re)creations, 0 updates, 0 removals to 0 collections
"""
        self.line_contains_debug = """2012-10-02 01:20:00,008 DEBUG [com.riavera.ejb.session.EventDispatcherBean] (DefaultQuartzScheduler_Worker-7)  getting pending events"""
        self.line_contains_info = """2012-10-02 01:22:04,575 INFO  [com.riavera.ejb.session.GeoBean] (WorkerThread#1[192.168.20.71:10198])  found country US for ip 72.14.199.102"""
        self.line_contains_warn = """2012-10-02 00:01:32,081 WARN  [com.riavera.ejb.session.MobileDeviceBean] (WorkerThread#1[192.168.20.71:50682]) ::nnapp_fi_in::99: extra device attribute supplied but not processed: OS=IOS"""
        self.line_contains_error = """2012-10-02 00:01:32,117 ERROR [com.navahonetworks.ejb.session.app.LoginUserLogicBean] (WorkerThread#5[192.168.20.71:10806])  couldn't get loginUserSF by handle: Could not activate; failed to restore state; nested exception is: 
            java.rmi.NoSuchObjectException: Could not activate; failed to restore state"""
        self.first_line_stacktrace = """2012-10-02 00:01:32,119 DEBUG [org.jboss.ejb.plugins.AbstractInstanceCache] (WorkerThread#5[192.168.20.71:10806])  Activation failure: javax.ejb.EJBException: Could not activate; failed to restore state"""
        self.other_stacktrace_line = """        at org.jboss.ejb.plugins.StatefulSessionFilePersistenceManager.activateSession(StatefulSessionFilePersistenceManager.java:343) [:6.1.0.Final]"""
        self.other_stacktrace_line_2 = """Caused by: java.io.FileNotFoundException: /usr/local/java/jboss-6.1.0.Final/server/prod.ejb/tmp/sessions/LoginUserSF-h7rxw4f1-p6/h7s6ck39-ph.ser (No such file or directory)"""
        self.line_after_stacktrace = """
"""
        self.line_contains_debug_and_fail = """2012-10-02 00:01:32,119 DEBUG [org.jboss.ejb.plugins.AbstractInstanceCache] (WorkerThread#5[192.168.20.71:10806])  Activation failure: javax.ejb.EJBException: Could not activate; failed to restore state"""


    def teatDown(self):
        self.filtering_words = []
        self.log_dump = None
        self.line_contains_debug = None
        self.line_contains_info = None
        self.line_contains_warn = None
        self.line_contains_error = None
        self.first_line_stacktrace = None
        self.other_stacktrace_line = None
        self.other_stacktrace_line_2 = None
        self.line_after_stacktrace = None
        self.line_contains_debug_and_fail = None


    def test_one_line_has_no_filtering_words_returns_false(self):
        test_line = "TEST line"
        log_filename = "test.log"
        filtered_log_filename = "filtered_test.log"
        ejb_filter = JbossEjbFilter(log_filename, filtered_log_filename, self.filtering_words)
        self.assertFalse(ejb_filter.filter_log_each_line(test_line))


    def test_one_line_has_INFO_filtering_words_returns_the_line(self):
        test_line = self.line_contains_info
        log_filename = "test.log"
        filtered_log_filename = "filtered_test.log"
        ejb_filter = JbossEjbFilter(log_filename, filtered_log_filename, self.filtering_words)
        self.assertEqual(test_line, ejb_filter.filter_log_each_line(test_line))


    def test_one_line_has_ERROR_filtering_words_returns_the_line(self):
        test_line = self.line_contains_error
        log_filename = "test.log"
        filtered_log_filename = "filtered_test.log"
        ejb_filter = JbossEjbFilter(log_filename, filtered_log_filename, self.filtering_words)
        self.assertEqual(test_line, ejb_filter.filter_log_each_line(test_line))


    def test_one_line_has_WARN_filtering_words_returns_the_line(self):
        test_line = self.line_contains_warn
        log_filename = "test.log"
        filtered_log_filename = "filtered_test.log"
        ejb_filter = JbossEjbFilter(log_filename, filtered_log_filename, self.filtering_words)
        self.assertEqual(test_line, ejb_filter.filter_log_each_line(test_line))


    def test_one_line_has_stacktrace_returns_the_line(self):
        test_line = self.other_stacktrace_line
        log_filename = "test.log"
        filtered_log_filename = "filtered_test.log"
        ejb_filter = JbossEjbFilter(log_filename, filtered_log_filename, self.filtering_words)
        self.assertEqual(test_line, ejb_filter.filter_log_each_line(test_line))


    def test_write_line_into_filtered_file_which_does_not_exist_returns_true(self):
        test_line = self.other_stacktrace_line
        log_filename = "test.log"
        filtered_log_filename = "filtered_test.log"
        ejb_filter = JbossEjbFilter(log_filename, filtered_log_filename, self.filtering_words)
        self.assertTrue(ejb_filter.write_filtered_log(test_line))

    def test_is_stacktrace_empty_returns_false(self):
        test_line = self.line_after_stacktrace
        log_filename = "test.log"
        filtered_log_filename = "filtered_test.log"
        ejb_filter = JbossEjbFilter(log_filename, filtered_log_filename, self.filtering_words)
        self.assertFalse(ejb_filter.is_stacktrace(test_line))

    def test_is_stacktrace_line_starts_with_tab_at_returns_true(self):
        test_line = self.other_stacktrace_line
        log_filename = "test.log"
        filtered_log_filename = "filtered_test.log"
        fake_line_starts_with = ["        at", "Caused by: "]
        ejb_filter = JbossEjbFilter(log_filename, filtered_log_filename, self.filtering_words)
        self.assertTrue(ejb_filter.is_stacktrace(test_line, fake_line_starts_with))

    def test_is_stacktrace_line_starts_with_caused_by_returns_true(self):
        test_line = self.other_stacktrace_line_2
        log_filename = "test.log"
        filtered_log_filename = "filtered_test.log"
        ejb_filter = JbossEjbFilter(log_filename, filtered_log_filename, self.filtering_words)
        self.assertTrue(ejb_filter.is_stacktrace(test_line))

    def test_is_stacktrace_non_stacktrace_line_returns_false(self):
        test_line = self.line_contains_error
        log_filename = "test.log"
        filtered_log_filename = "filtered_test.log"
        ejb_filter = JbossEjbFilter(log_filename, filtered_log_filename, self.filtering_words)
        self.assertFalse(ejb_filter.is_stacktrace(test_line))

if __name__ == '__main__':
    unittest.main()
