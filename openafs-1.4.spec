%define _prefix /opt/bx
%define vendor_tag BX

Name: openafs
Version: 1.4.14
Release: 2
License: IBM Public License
Vendor: http://www.bx.psu.edu
BuildRoot: %{_tmppath}/%{name}-%{version}-root
Summary: openafs - OpenAFS distributed filesystem
URL: http://www.openafs.org
Source: %{name}-%{version}-src.tar.gz
Source1: openafs-client.xml
Source2: openafs-client.method
Source3: openafs-server.xml
Source4: openafs-server.method
Source5: openafs.conf.example

SUNW_Pkg: %{vendor_tag}%{name}

%description
OpenAFS distributed filesystem.


%prep
%setup -q

%build
CC=cc ./configure \
	--prefix=%{_prefix} \
	--sysconfdir=/etc/opt/bx \
	--localstatedir=/var/opt/bx \
	--with-krb5-conf=/usr/bin/krb5-config

%{__make} %{?_smp_mflags}


%install
rm -rf %{buildroot}
%{__make} install DESTDIR=%{buildroot}

# etc and var
%{_install} -m 0755 -d %{buildroot}/etc/opt/bx/openafs/
%{_install} -m 0644 %{SOURCE5} %{buildroot}/etc/opt/bx/openafs/
%{_install} -m 0755 -d %{buildroot}/etc/opt/bx/openafs/server/

%{_install} -m 0700 -d %{buildroot}/var/opt/bx/openafs/
%{_install} -m 0700 -d %{buildroot}/var/opt/bx/openafs/db/
%{_install} -m 0755 -d %{buildroot}/var/opt/bx/openafs/logs/
%{_install} -m 0700 -d %{buildroot}/var/opt/bx/openafs/cache

# manifests
%{_install} -m 0755 -d %{buildroot}/var/svc/manifest/site/
%{_install} -m 0644 %{SOURCE1} %{buildroot}/var/svc/manifest/site/
%{_install} -m 0644 %{SOURCE3} %{buildroot}/var/svc/manifest/site/

# methods
%{_install} -m 0755 -d %{buildroot}/lib/svc/method/
%{_install} -m 0755 %{SOURCE2} %{buildroot}/lib/svc/method/
%{_install} -m 0755 %{SOURCE4} %{buildroot}/lib/svc/method/

# kernel module
%ifarch amd64
%{_install} -m 0755 -d %{buildroot}/kernel/fs/amd64
%{_install} -m 0644 %{buildroot}/opt/bx/lib/openafs/libafs64.nonfs.o %{buildroot}/kernel/fs/amd64/afs
%endif
%ifarch sparcv9
%{_install} -m 0755 -d %{buildroot}/kernel/fs/sparcv9
%{_install} -m 0644 %{buildroot}/opt/bx/lib/openafs/libafs64.nonfs.o %{buildroot}/kernel/fs/sparcv9/afs
%endif


%clean
rm -rf %{buildroot}


%files
%defattr (-, root, root)
%{_prefix}/*
/var/svc/manifest/site/*
/lib/svc/method/*

%ifarch amd64
/kernel/fs/amd64/afs
%endif

%ifarch sparcv9 
/kernel/fs/sparcv9/afs
%endif

/var/opt/bx/openafs
/etc/opt/bx/openafs/server
%config(noreplace) /etc/opt/bx/openafs/openafs.conf

%post
/usr/sbin/svccfg import /var/svc/manifest/site/openafs-client.xml
/usr/sbin/svccfg import /var/svc/manifest/site/openafs-server.xml

%changelog
* Wed Mar 16 2011 Andy Cobaugh <phalenor@bx.psu.edu> - 1.4.14
- Initial version
