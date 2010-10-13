%define _prefix /opt/bx
%define vendor_tag BX

Name: openafs
Version: 1.4.12.1
License: IBM Public License
Vendor: http://www.bx.psu.edu
BuildRoot: %{_tmppath}/%{name}-%{version}-root
Summary: OpenAFS
URL: http://www.openafs.org
Source: %{name}-%{version}-src.tar.gz

%define SUNW_Pkg %{vendor_tag}%{name}

%description
OpenAFS


%prep
%setup -q

%build
CC=cc ./configure \
	--prefix=%{_prefix} \
	--sysconfdir=/etc/opt/bx \
	--localstatedir=/var/opt/bx \
	--with-krb5-conf=/usr/bin/krb5-config

%{__make}


%install
%{__make} install DESTDIR=%{buildroot}


%clean
rm -rf %{buildroot}


%files
%defattr (-, root, root)
%{_prefix}/*


%changelog
* Wed Oct 13 2010 Andy Cobaugh <phalenor@bx.psu.edu> - 1.4.12
- Initial version
