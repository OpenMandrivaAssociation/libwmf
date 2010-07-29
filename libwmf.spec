%define	name	libwmf
%define	version	0.2.8.4
%define api 0.2
%define major	7
%define libname %mklibname wmf%{api}_ %major
%define develname %mklibname -d wmf

Summary:	A library to convert wmf files
Name:		%{name}
Version:	%{version}
Release:	%mkrel 22
License:	GPL
Group:		Text tools
BuildRequires:	freetype2-devel
BuildRequires:	libgdk_pixbuf2.0-devel
BuildRequires:	png-devel 
BuildRequires:	libexpat-devel
BuildRequires:	libjpeg-devel
BuildRequires:	libx11-devel
URL:		http://sourceforge.net/projects/wvware/
Source:		http://download.sourceforge.net/wvware/%{name}-%{version}.tar.bz2
Patch:		libwmf-0.2.7-libwmf-config.patch
Patch1:		libwmf-0.2.8.3-CAN-2004-0941.patch
Patch2:		libwmf-0.2.8.3-CAN-2004-0990.patch
Patch3:		libwmf-0.2.8.4-intoverflow.patch
Patch4:		libwmf-0.2.8.4-CVE2007-2756.patch
Patch5:		libwmf-0.2.8.4-rh-CVE-2009-1364.diff
Patch6:		libwmf-0.2.8.4-gdk2.22.patch
BuildRoot:	%{_tmppath}/%{name}-buildroot

%description
libwmf is a library for unix like machines that can convert wmf
files into other formats, currently it supports a gd binding
to convert to gif, and an X one to draw direct to an X window
or pixmap.

%package -n %libname
Summary:	A library to convert wmf files. - library files
Group:		System/Libraries
Requires:	urw-fonts
Conflicts:	%{name} < 0.2.8.4-7
Requires(post):	gdk-pixbuf2.0
Requires(postun): gdk-pixbuf2.0

%description -n %libname
This package contains the library needed to run programs dynamically
linked with libwmf.

%package -n %develname
Summary:	A library to convert wmf files. - development environment
Group:		Development/C
Requires:	%{libname} = %{version}-%{release}
Provides:	libwmf-devel = %{version}-%{release}
Provides:	libwmf0.2-devel = %{version}-%{release}
Obsoletes:	libwmf-devel < %{version}-%{release}
Obsoletes:	%{_lib}wmf0.2_7-devel < 0.2.8.4-21

%description -n %develname
libwmf is a library for unix like machines that can convert wmf
files into other formats, currently it supports a gd binding
to convert to gif, and an X one to draw direct to an X window
or pixmap.

Install libwmf-devel if you need to compile an application with libwmf
support.

%prep
%setup -q -n %{name}-%{version}
%patch -p1 -b .fpons
%patch1 -p1 -b .can-2004-0941
%patch2 -p1 -b .can-2004-0990
%patch3 -p1 -b .cve-2006-3376
%patch4 -p1 -b .cve-2007-2756
%patch5 -p0 -b .CVE-2009-1364
%patch6 -p0 -b .gdk222

%build
autoreconf -fi
%configure2_5x --disable-static
%make

%install
rm -rf %{buildroot} installed-docs
%makeinstall_std

mv %{buildroot}%{_prefix}/share/doc/* installed-docs

#gw no windows line endings
perl -pi -e 's/\r//' $(find installed-docs -type f )

# remove anything relevant to fonts.
rm -rf %{buildroot}%{_bindir}/libwmf-fontmap %{buildroot}%{_datadir}/libwmf
# remove static libraries.
rm -f %{buildroot}%{_libdir}/libwmf*.a %{buildroot}%{_libdir}/gtk-*/*/*/*.a

# multiarch support
%multiarch_binaries %{buildroot}%{_bindir}/libwmf-config

%clean
rm -rf %{buildroot}

%post -n %libname
%if %mdkversion < 200900
/sbin/ldconfig
%endif
%_bindir/gdk-pixbuf-query-loaders --update-cache

%postun -n %libname
%if %mdkversion < 200900
/sbin/ldconfig
%endif
if [ -x  %_bindir/gdk-pixbuf-query-loaders ]; then
%_bindir/gdk-pixbuf-query-loaders --update-cache
fi

%files
# beware not to take gd files here!
%defattr(-,root,root)
%docdir COPYING
%{_bindir}/wmf2*

%files -n %libname
# beware not to take gd files here!
%defattr(-,root,root)
%doc COPYING
%{_libdir}/libwmf*-%{api}.so.%{major}*
%{_libdir}/gdk-pixbuf-2.0/*/loaders/io-wmf.*

%files -n %develname
# beware not to take gd files here!
%defattr(-,root,root)
%doc COPYING CREDITS README NEWS
%doc installed-docs/*
%doc ChangeLog
%{_bindir}/libwmf-config
%multiarch %{multiarch_bindir}/libwmf-config
%{_libdir}/libwmf.la
%{_libdir}/libwmf.so
%{_libdir}/libwmflite.la
%{_libdir}/libwmflite.so
%{_includedir}/libwmf
