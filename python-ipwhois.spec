# Conditional build:
%bcond_without	python2 # CPython 2.x module
%bcond_without	python3 # CPython 3.x module

%define		module		ipwhois
%define		egg_name	ipwhois
%define		pypi_name	ipwhois
Summary:	Retrieve and parse whois data for IPv4 and IPv6 addresses
Name:		python-%{module}
Version:	1.2.0
Release:	6
License:	BSD-like
Group:		Libraries/Python
Source0:	https://pypi.debian.net/ipwhois/ipwhois-1.2.0.tar.gz
# Source0-md5:	29c322d1c812793a48378b738f6e9b04
Patch0:		python.patch
URL:		https://github.com/secynic/ipwhois
%if %{with python2}
BuildRequires:	python-modules >= 1:2.5
BuildRequires:	python-setuptools
%endif
%if %{with python3}
BuildRequires:	python3-modules >= 1:3.2
BuildRequires:	python3-setuptools
%endif
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.714
Requires:	python-modules >= 1:2.5
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
pwhois is a Python package focused on retrieving and parsing whois data for IPv4 and IPv6 addresses.

%package -n python3-%{module}
Summary:	Retrieve and parse whois data for IPv4 and IPv6 addresses
Group:		Libraries/Python
Requires:	python3-modules >= 1:3.2

%description -n python3-%{module}
pwhois is a Python package focused on retrieving and parsing whois data for IPv4 and IPv6 addresses.

%prep
%setup -q -n %{pypi_name}-%{version}
%patch -P 0 -p1

%build
%if %{with python2}
%py_build
%endif

%if %{with python3}
%py3_build
%endif

%install
rm -rf $RPM_BUILD_ROOT

%if %{with python2}
%py_install
%py_postclean
%endif

%if %{with python3}
# Remove python2 artefacts
%{__rm} -f $RPM_BUILD_ROOT%{_bindir}/*
%py3_install
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%if %{with python2}
%files
%defattr(644,root,root,755)
%doc *.rst
%{py_sitescriptdir}/%{module}
%{py_sitescriptdir}/%{egg_name}-%{version}-py*.egg-info
%endif

%if %{with python3}
%files -n python3-%{module}
%defattr(644,root,root,755)
%doc *.rst
%attr(755,root,root) %{_bindir}/ipwhois_cli.py
%attr(755,root,root) %{_bindir}/ipwhois_utils_cli.py
%{py3_sitescriptdir}/%{module}
%{py3_sitescriptdir}/%{egg_name}-%{version}-py*.egg-info
%endif
