Summary:	ODBC
Summary(pl):	ODBC
Name:		ODBC
Version:	1.8	
Release:	1
License:	GPL
Group:		Libraries
Group(pl):	Biblioteki
#site:		
#path:		
BuildRequires:	XFree86-devel
BuildRequires:	qt-devel
Source:		unix%name-%version.tar.gz
Buildroot:	/tmp/%{name}-%{version}-root

%define	_prefix	/usr/X11R6
%define	_sysconfdir	/etc

%description

%description -l pl

# optional package =====================
%package devel
Summary:	ODBC
Summary(pl):	ODBC
Group:		Development/Libraries
Group(pl):	Programowanie/Biblioteki

%description devel
%description -l pl devel

# end of optional package ==============

%prep
%setup -q -n unix%name-%version

%build
./configure --prefix=%{_prefix} \
	--enable-gui \
	--enable-threads \
	--enable-drivers \
	--enable-shared \
	--enable-static \
	--disable-fast-install \
	--with-qt-dir=%{_prefix} 
make RPM_OPT_FLAGS="$RPM_OPT_FLAGS"

%install
rm -rf $RPM_BUILD_ROOT
make prefix=$RPM_BUILD_ROOT%{_prefix} install

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc
%attr(755,root,root) %{_libdir}/lib*.so.*
%attr(755,root,root) %{_bindir}/dltest
%attr(755,root,root) %{_bindir}/isql
%attr(755,root,root) %{_bindir}/odbcinst
%config %{_sysconfdir}/odbc.ini
%config %{_sysconfdir}/odbcinst.ini
# optional package

%files devel
%defattr(644,root,root,755)
%doc
%attr(755,root,root) %{_libdir}/lib*.so
%attr(755,root,root) %{_libdir}/lib*.la
%attr(644,root,root) %{_libdir}/lib*.a
%attr(644,root,root) %{_includedir}/odbc*.h
%attr(644,root,root) %{_includedir}/sql*.h
#end of optional package
