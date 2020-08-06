Name:           mytest
Version:        1.0
Release:        1%{?dist}
Summary:        Service managing

Group:          Utilities
License:        GPL
URL:            http://www.mypage.com
Source0:        mytest-1.0.tar.gz
BuildArch:      noarch
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

%description    A service managing app

%prep
%setup -q

%build

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT/opt/mytest
install app.py $RPM_BUILD_ROOT/opt/mytest/app.py

%clean
rm -rf $RPM_BUILD_ROOT

%files
%dir /opt/mytest
%defattr(-,root,root,-)
/opt/mytest/app.py
/opt/mytest/app.pyc
/opt/mytest/app.pyo

%post
chmod 755 -R /opt/mytest
cd /opt/mytest
python3 app.py
