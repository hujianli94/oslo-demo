#   Copyright 2012-2013 OpenStack Foundation
#
#   Licensed under the Apache License, Version 2.0 (the "License"); you may
#   not use this file except in compliance with the License. You may obtain
#   a copy of the License at
#
#        http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#   WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#   License for the specific language governing permissions and limitations
#   under the License.
#
import oslo_i18n

_translators = oslo_i18n.TranslatorFactory(domain='ws_monitor')

# The primary translation function using the well-known name "_"
_ = _translators.primary

# Translators for log levels.
#
# The abbreviated names are meant to reflect the usual use of a short
# name like '_'. The "L" is for "log" and the other letter comes from
# the level.
_LI = _translators.log_info
_LW = _translators.log_warning
_LE = _translators.log_error
_LC = _translators.log_critical


# To enable logging translations, import and call enable()
# 调用 oslo_i18n.enable_lazy() 来启用延迟翻译。
# 这意味着只有在实际需要使用翻译后的字符串时，才会进行翻译操作。这可以提高性能，尤其是在日志记录中。
def enable():
    oslo_i18n.enable_lazy()
