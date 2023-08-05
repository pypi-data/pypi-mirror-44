# Copyright 2017, Juniper Networks, Inc
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

from django.conf.urls import url

from neutron_fwaas_dashboard.dashboards.project.firewalls_v2 import views

# TODO(Sarath Mekala) : Fix 'firewall' --> 'firewallgroup' in URLs as
# well as in other places.
urlpatterns = [
    url(r'^$', views.IndexView.as_view(), name='index'),
    url(r'^\?tab=fwtabs__firewalls$',
        views.IndexView.as_view(), name='firewalls'),
    url(r'^\?tab=fwtabs__rules$', views.IndexView.as_view(), name='rules'),
    url(r'^\?tab=fwtabs__policies$',
        views.IndexView.as_view(), name='policies'),
    url(r'^addrule$', views.AddRuleView.as_view(), name='addrule'),
    url(r'^addpolicy$', views.AddPolicyView.as_view(), name='addpolicy'),
    url(r'^addfirewallgroup$',
        views.AddFirewallGroupView.as_view(),
        name='addfirewallgroup'),
    url(r'^insertrule/(?P<policy_id>[^/]+)/$',
        views.InsertRuleToPolicyView.as_view(), name='insertrule'),
    url(r'^removerule/(?P<policy_id>[^/]+)/$',
        views.RemoveRuleFromPolicyView.as_view(), name='removerule'),
    url(r'^updaterule/(?P<rule_id>[^/]+)/$',
        views.UpdateRuleView.as_view(), name='updaterule'),
    url(r'^updatepolicy/(?P<policy_id>[^/]+)/$',
        views.UpdatePolicyView.as_view(), name='updatepolicy'),
    url(r'^updatefirewall/(?P<firewall_id>[^/]+)/$',
        views.UpdateFirewallView.as_view(), name='updatefirewall'),
    url(r'^addport/(?P<firewallgroup_id>[^/]+)/$',
        views.AddPortView.as_view(), name='addport'),
    url(r'^removeport/(?P<firewallgroup_id>[^/]+)/$',
        views.RemovePortView.as_view(), name='removeport'),
    url(r'^rule/(?P<rule_id>[^/]+)/$',
        views.RuleDetailsView.as_view(), name='ruledetails'),
    url(r'^policy/(?P<policy_id>[^/]+)/$',
        views.PolicyDetailsView.as_view(), name='policydetails'),
    url(r'^firewallgroup/(?P<firewallgroup_id>[^/]+)/$',
        views.FirewallGroupDetailsView.as_view(), name='firewallgroupdetails'),
]
