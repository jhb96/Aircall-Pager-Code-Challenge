import unittest
from unittest.mock import MagicMock
import sys, os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))
print(sys.path)
from domain.services.pager_service import ServicePager
from domain.models.monitored_service import MonitoredService

from domain.models.level import Level
from domain.models.email_target import EmailTarget
from domain.models.slack_target import SlackTarget
from domain.models.sms_target import SMSTarget

from domain.models.escalation_policy import EscalationPolicy
from domain.models.monitored_service import MonitoredService

# ---------------- USE CASE 1 ---------------- #
"""
Given a Monitored Service in a Healthy State,
when the Pager receives an Alert related to this Monitored Service,
then the Monitored Service becomes Unhealthy,
the Pager notifies all targets of the first level of the escalation policy,
and sets a 15-minutes acknowledgement delay
"""

class TestServicePager(unittest.TestCase):
    def setUp(self):
        # Create random MS
        self.service = MonitoredService('')
        # Mock adapters
        timer_mock = MagicMock()
        escalation_mock = MagicMock()
        email_mock = MagicMock()
        slack_mock = MagicMock()
        sms_mock = MagicMock()
        repo_mock = MagicMock()
        
        # Mock behaviors
        repo_mock.save = MagicMock()
        repo_mock.get.return_value = self.service
        escalation_mock.get.return_value = EscalationPolicy([
            Level(0, [EmailTarget('demoA@aircall.com'), EmailTarget('demoB@aircall.com')])
        ])
        
        email_mock.notify = MagicMock()
        timer_mock.add_timeout = MagicMock()


        # Create an instance of ServicePager with mocked adapters
        self.pager = ServicePager(
            timer_system = timer_mock,
            escalation_system = escalation_mock,
            mail_system = email_mock,
            sms_system = sms_mock,
            slack_system = slack_mock,
            repository = repo_mock
        )
        
        
    def __adapt_mocks(self, service: MonitoredService, policy: EscalationPolicy = None):
        self.service = service
        self.pager.repository.get.return_value = service
        
        if policy:
            self.pager.escalation_service.get.return_value = policy
        
        
        
    # Test use case 1
    def test_1(self):
        """
        Given a Monitored Service in a Healthy State,
        when the Pager receives an Alert related to this Monitored Service,
        then the Monitored Service becomes Unhealthy,
        the Pager notifies all targets of the first level of the escalation policy,
        and sets a 15-minutes acknowledgement delay
        """

        service = MonitoredService("service-1")
        self.__adapt_mocks(service)
        message = "Alert!"

        # Simulate an alert
        self.pager.handle_alert(service.id, message)
        
        # Check that the service is now unhealthy
        self.assertEqual(self.service.status, 'unhealthy')
        self.assertEqual(self.service.alert_msg, message)
        self.assertFalse(self.service.acknowledged)

        # Repo worked?
        self.assertEqual(self.pager.repository.get.call_count, 1)
        self.assertEqual(self.pager.repository.save.call_count, 1)
        
        # Alert send?
        self.assertEqual(self.pager.mail_service.notify.call_count, 2)
        
        # Timeout set?
        self.assertEqual(self.pager.time_service.add_timeout.call_count, 1)
        self.pager.time_service.add_timeout.assert_called_with(service.id, 15)
        
    # Test use case 2
    def test_2(self):
        """
        Given a Monitored Service in an Unhealthy State,
        the corresponding Alert is not Acknowledged
        and the last level has not been notified,
        when the Pager receives the Acknowledgement Timeout,
        then the Pager notifies all targets of the next level of the escalation policy
        and sets a 15-minutes acknowledgement delay.
        """

        service = MonitoredService("service-2")
        service.status = 'unhealthy'
        policy = EscalationPolicy([
            Level(0, [EmailTarget('demoA@aircall.com'), EmailTarget('demoB@aircall.com')]),
            Level(1, [EmailTarget('1234567890')])
        ])
        
        self.__adapt_mocks(service, policy)
        
        self.pager.handle_timeout(service.id)
        
        # Check that the service is now unhealthy
        self.assertEqual(self.service.status, 'unhealthy')
        self.assertFalse(self.service.acknowledged)
        self.assertEqual(self.service.current_level, 1)
        
        # Repo works?
        self.assertEqual(self.pager.repository.get.call_count, 1)
        self.assertEqual(self.pager.repository.save.call_count, 1)
        # Not notify any target
        self.assertEqual(self.pager.mail_service.notify.call_count, 1)
        # Set timeout
        self.assertEqual(self.pager.time_service.add_timeout.call_count, 1)
        
    
    # Test use case 3
    def test3(self):
        """
        Given a Monitored Service in an Unhealthy State
        when the Pager receives the Acknowledgement
        and later receives the Acknowledgement Timeout,
        then the Pager doesn't notify any Target
        and doesn't set an acknowledgement delay.
        """
        
        # Prepare MS
        service = MonitoredService("service-3")
        service.status = 'unhealthy'
        policy = EscalationPolicy([
            Level(0, [EmailTarget('demoA@aircall.com'), EmailTarget('demoB@aircall.com')]),
            Level(1, [EmailTarget('1234567890')])
        ])
        
        self.__adapt_mocks(service, policy)
        
        # ------- STEP 1 - Acknowledge ------- #
        self.pager.handle_acknowledge(service.id)
        # Check that the service is now acknowledged
        self.assertTrue(self.service.acknowledged)
        self.assertEqual(self.service.status, 'unhealthy')
        # Repo works?
        self.assertEqual(self.pager.repository.get.call_count, 1)
        self.assertEqual(self.pager.repository.save.call_count, 1)
        
        # ------- STEP 2 - Timeout ------- #
        # Not notify any target
        self.pager.handle_timeout(service.id)
        self.assertEqual(self.pager.mail_service.notify.call_count, 0)
        self.assertEqual(self.pager.sms_service.notify.call_count, 0)
        self.assertEqual(self.pager.time_service.add_timeout.call_count, 0)
        #Repo
        self.assertEqual(self.pager.repository.get.call_count, 2)
        
    
    # Test use case 4
    def test_4(self):
        """
        Given a Monitored Service in an Unhealthy State,
        when the Pager receives an Alert related to this Monitored Service,
        then the Pager doesn’t notify any Target
        and doesn’t set an acknowledgement delay
        """
        # Prepare MS
        service = MonitoredService("service-4")
        service.status = 'unhealthy'
        
        self.__adapt_mocks(service)
        
        self.pager.handle_alert(service.id, "Alert!")
        
        # Repo?
        # Monitor service is loaded
        self.assertEqual(self.pager.repository.get.call_count, 1)
        # But not saved
        self.assertEqual(self.pager.repository.save.call_count, 0)
        
        # And not is notified
        self.assertEqual(self.pager.mail_service.notify.call_count, 0)
        self.assertEqual(self.pager.sms_service.notify.call_count, 0)
        
        # And not acknowledge timeout is set
        self.assertEqual(self.pager.time_service.add_timeout.call_count, 0)
        
    
    # Test use case 5
    def test_5(self):
        """
        Given a Monitored Service in an Unhealthy State,
        when the Pager receives a Healthy event related to this Monitored Service
        and later receives the Acknowledgement Timeout,
        then the Monitored Service becomes Healthy,
        the Pager doesn’t notify any Target
        and doesn’t set an acknowledgement delay
        """

        # Prepare MS
        service = MonitoredService("service-5")
        service.status = 'unhealthy'
        
        self.__adapt_mocks(service)
        
        # ------- STEP 1 - Healthy event received ------- #
        self.pager.handle_healthy(service.id)
        
        # Check MS reset
        self.assertEqual(self.service.status, 'healthy')
        self.assertEqual(self.service.alert_msg, "")
        self.assertFalse(self.service.acknowledged)
        self.assertEqual(self.service.current_level, 0)
        
        # Repo works?
        self.assertEqual(self.pager.repository.get.call_count, 1)
        self.assertEqual(self.pager.repository.save.call_count, 1)
        
        
        # ------- STEP 2 - Acknowledgemnt timeout ------- #
        # Not notify any target
        self.pager.handle_timeout(service.id)
        self.assertEqual(self.pager.mail_service.notify.call_count, 0)
        self.assertEqual(self.pager.sms_service.notify.call_count, 0)
        # Not timeout set
        self.assertEqual(self.pager.time_service.add_timeout.call_count, 0)
        # Repo
        self.assertEqual(self.pager.repository.get.call_count, 2)
        
    
    def test_slack_notify(self):
        """
        Test Slack.
        When send and alert and a target is a SlackTarget the service should notify the target
        """

        service = MonitoredService("service-6")
        policy = EscalationPolicy([
            Level(0, [SlackTarget('slack.com/aircall', '@errors')])
        ])
        
        self.__adapt_mocks(service, policy)
        
        self.pager.handle_alert(service.id, "Alert to Slack!")
        
        # Only 1 call (slack notify)
        self.assertEqual(self.pager.slack_service.notify.call_count, 1)
        # Check the call arguments
        self.pager.slack_service.notify.assert_called_with(policy.levels[0].targets[0], service, "Alert to Slack!")
        
        

    
        
if __name__ == "__main__":
    unittest.main()
