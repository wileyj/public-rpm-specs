%include %{_rpmconfigdir}/macros.d/macros.python27
%global srcname celery

Name:           python27-%{srcname}
Version:        3.1.17
Release:        2.%{dist}
Summary:        Distributed Task Queue 
Group:          Development/Languages
License:        BSD
Packager: %{packager}
Vendor: %{vendor}
URL:            http://pypi.python.org/pypi/celery
Source0:        %{srcname}-%{version}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires:  python27-devel
BuildRequires:  python27-setuptools
Requires:       python27
Requires:       jython

%description
Task queues are used as a mechanism to distribute work across threads or machines.
A task queue’s input is a unit of work, called a task, dedicated worker processes then constantly monitor the queue for new work to perform.
Celery communicates via messages, usually using a broker to mediate between clients and workers. To initiate a task a client puts a message on the queue, the broker then delivers the message to a worker.
A Celery system can consist of multiple workers and brokers, giving way to high availability and horizontal scaling.
Celery is a library written in Python, but the protocol can be implemented in any language. So far there’s RCelery for the Ruby programming language, and a PHP client, but language interoperability can also be achieved by using webhooks.

%prep
%setup -q -n %{srcname}-%{version}

%build
%{__python27} setup.py build

%install
rm -rf $RPM_BUILD_ROOT
%{__python27} setup.py install --skip-build --root $RPM_BUILD_ROOT
 
%clean
[ "%{buildroot}" != "/" ] && %__rm -rf %{buildroot}
[ "%{_builddir}/%{srcname}-%{version}" != "/" ] && %__rm -rf %{_builddir}/%{srcname}-%{version}
[ "%{_builddir}/%{srcname}" != "/" ] && %__rm -rf %{_builddir}/%{srcname}

%files
%defattr(-,root,root,-)
%doc Changelog LICENSE
%{python27_sitelib}/%{srcname}/
%{python27_sitelib}/%{srcname}*.egg-info
%{_bindir}/celery*

%changelog

