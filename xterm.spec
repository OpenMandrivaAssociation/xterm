# THIS PACKAGE IS HOSTED AT MANDRIVA SVN
# PLEASE DO NOT UPLOAD DIRECTLY BEFORE COMMIT

%define	Summary	The standard terminal emulator for the X Window System

Summary:	%{Summary}
Name:		xterm
Version:	215
Release:	%mkrel 6

Source0:	ftp://dickey.his.com/xterm/%{name}-%{version}.tar.bz2
Source11:	%{name}-16x16.png
Source12:	%{name}-32x32.png
Source13:	%{name}-48x48.png
Patch1:		xterm-199-alt-meta-mod.patch
Patch3:		xterm-197-alt-keysym-index.patch
Url:		http://dickey.his.com/xterm
License:	MIT
Group:		Terminals
BuildRequires:	X11-devel 
BuildRequires: libtermcap-devel
BuildRoot: %{_tmppath}/%{name}-%{version}-%{version}-buildroot
Conflicts: XFree86 < 3.3.6-13mdk
Requires: luit
Requires(post,postun):	/usr/sbin/update-alternatives

%description
The XTerm program is the standard terminal emulator for the X Window System. It
provides DEC VT102/VT220 and Tektronix 4014 compatible terminals for programs
that can't use the window system directly. If the underlying operating system
supports terminal resizing capabilities (for example, the SIGWINCH signal in
systems derived from 4.3bsd), xterm will use the facilities to notify programs
running in the window whenever it is resized.

%prep
%setup -q
%patch1 -p1 -b .alt-meta-mod
%patch3 -p1 -b .alt-keysym-index

%build
%configure \
   --enable-wide-chars \
   --x-includes=%{_includedir}/freetype2 \
   --enable-luit

%make

%install
rm -rf $RPM_BUILD_ROOT
make install appsdir=$RPM_BUILD_ROOT%{_libdir}/X11/app-defaults \
		bindir=$RPM_BUILD_ROOT%{_bindir} \
		mandir=$RPM_BUILD_ROOT%{_mandir}/man1 

# NOTE: encodingMode: locale means to follow the charset encoding of the
# locale. A quite complete unicode font is set as the default (instead of the
# very poor "fixed" one). a quick cat is used instead of patching the sources;
# it shoulmd be made the default imho
# locale: true means to use luit to convert locale encoding to unicode
# for display.
# luit support is needed for it to work -- pablo
cat << EOF >> $RPM_BUILD_ROOT%{_libdir}/X11/app-defaults/XTerm
*.vt100.font: -misc-fixed-medium-r-normal--15-140-75-75-c-90-iso10646-1
*.vt100.encodingMode: locale
*.locale: true
*.PtyInitialErase: on
*.backarrowKeyIsErase: on
EOF

mkdir -p $RPM_BUILD_ROOT%{_menudir}
cat << EOF > $RPM_BUILD_ROOT%{_menudir}/%{name}
?package(%{name}):\
  needs=X11\
  section="System/Terminals"\
  title="XTerm"\
  longtitle="%{Summary}"\
  command="%{_bindir}/xterm -name Terminal"\
  icon="xterm-terminal.png" xdg="true"
EOF
mkdir -p $RPM_BUILD_ROOT%{_datadir}/applications
cat > $RPM_BUILD_ROOT%{_datadir}/applications/mandriva-%{name}.desktop << EOF
[Desktop Entry]
Encoding=UTF-8
Name=XTerm
Comment=%Summary
Exec=%{name} -name Terminal
Icon=xterm-terminal
Terminal=false
Type=Application
StartupNotify=true
Categories=X-MandrivaLinux-System-Terminals;TerminalEmulator;System;
EOF

install -m644 %{SOURCE11} -D $RPM_BUILD_ROOT%{_miconsdir}/xterm-terminal.png
install -m644 %{SOURCE12} -D $RPM_BUILD_ROOT%{_iconsdir}/xterm-terminal.png
install -m644 %{SOURCE13} -D $RPM_BUILD_ROOT%{_liconsdir}/xterm-terminal.png

%if 0
## strange, if xterm isn't launched with -name xxxx parameter it doesn't
## take in account the ressources --> wrong font in unicode mode --> segfault
## there is not time to fix the sources; using a script to ensure there
## is always a -nae xxxx used (pablo)
mv $RPM_BUILD_ROOT%{_bindir}/xterm $RPM_BUILD_ROOT%{_bindir}/xterm.real
cat << EOF >> $RPM_BUILD_ROOT%{_bindir}/xterm
#!/bin/bash

if echo "\$@" | grep -- '-name' >&/dev/null ; then
	 exec %{_bindir}/xterm.real "\$@"
else exec %{_bindir}/xterm.real -name Terminal "\$@"
fi
EOF
chmod a+rx $r%{_bindir}/xterm
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%post
%update_menus
update-alternatives --install %{_bindir}/xvt xvt %{_bindir}/xterm 18 || :

%postun
%clean_menus
[[ "$1" = "0" ]] && update-alternatives --remove xvt %{_bindir}/xterm || :

%files
%defattr(-,root,root)
%doc AAA_README_VMS.txt MANIFEST README README.os390
%{_bindir}/*
%{_mandir}/*/*
%{_libdir}/X11/app-defaults/*
%_datadir/applications/mandriva-*
%{_menudir}/%{name}
%{_miconsdir}/xterm-terminal.png
%{_iconsdir}/xterm-terminal.png
%{_liconsdir}/xterm-terminal.png



