import re

old_print = print
DEBUG = False


def print(*args, **kwargs):
    if not DEBUG:
        return
    old_print(*args, **kwargs)


class IniSection:
    RegexSectionDefine = re.compile(r"^\[(\w+)\]")
    RegexVariable = re.compile(r"^(\w+)\s*=\s*(\S+)")

    def __init__(self, name, value):
        self._variableName = name
        self._variableValue = value
        self._prev = None
        self._next = None
        self._childHead = None
        self._childTail = None

    def addChild(self, name, value):
        if name is not None:
            new_child = IniSection(name, value)
            print(f"Adding child: {name} with value {value}")
            if self._childHead is None:
                self._childHead = new_child
                self._childTail = new_child
            else:
                self._childTail._next = new_child
                new_child._prev = self._childTail
                self._childTail = new_child
            return new_child
        return None

    def removeChild(self, child):
        current = self._childHead
        while current is not None:
            if current == child:
                if child._prev is not None:
                    child._prev._next = child._next
                else:
                    self._childHead = child._next
                if child._next is not None:
                    child._next._prev = child._prev
                else:
                    self._childTail = child._prev
                child._next = None
                child._prev = None
                return child
            current = current._next
        return None

    def getIntValue(self):
        try:
            return int(self._variableValue)
        except (ValueError, TypeError):
            return None

    def setIntValue(self, newValue):
        print(f"Setting int value: {newValue}")
        self._variableValue = str(newValue)
        return True

    def getFloatValue(self):
        try:
            return float(self._variableValue)
        except (ValueError, TypeError):
            return None

    def setFloatValue(self, newValue):
        print(f"Setting float value: {newValue}")
        self._variableValue = str(newValue)
        return True

    def readSection(self, sr):
        for line in sr:
            if self.RegexSectionDefine.match(line):
                return line
            match = self.RegexVariable.match(line)
            if match:
                self.addChild(match.group(1), match.group(2))
        return None

    def writeSection(self, sw):
        sw.write(f"[{self._variableName}]\n")
        current = self._childHead
        while current:
            value_to_write = (
                current._variableValue if current._variableValue is not None else ""
            )
            print(
                f"Writing variable: {current._variableName} with value {value_to_write}"
            )
            assert (
                current._variableValue == value_to_write
            ), f"Expected {value_to_write}, got {current._variableValue}"
            sw.write(f"{current._variableName} = {value_to_write}\n")
            current = current._next
        sw.write("\n")
        return 0


class IniFile:
    def __init__(self, filename):
        self._disposed = False
        self._dirty = False
        self._head = None
        self._tail = None
        self._filename = filename
        self.root_created = False
        self.construct(filename)

    def __del__(self):
        self.dispose(False)

    def dispose(self, disposing):
        if not self._disposed:
            if disposing:
                self._head = None
                self._tail = None
                self._filename = None
            self._disposed = True

    def getValue(self, section, variable, defaultParam):
        print(f"Entering getValue for section: {section}, variable: {variable}")
        iniSection = self.findSection(section)
        if iniSection is not None:
            iniSection2 = self.findVariable(iniSection, variable)
            if iniSection2 is not None:
                if isinstance(defaultParam, int):
                    value = iniSection2.getIntValue()
                    print(
                        f"Returning int value: {value if value is not None else defaultParam}"
                    )
                    return value if value is not None else defaultParam
                elif isinstance(defaultParam, float):
                    value = iniSection2.getFloatValue()
                    print(
                        f"Returning float value: {value if value is not None else defaultParam}"
                    )
                    return value if value is not None else defaultParam
                elif isinstance(defaultParam, bool):
                    intValue = iniSection2.getIntValue()
                    print(
                        f"Returning bool value: {intValue is not None and intValue!= 0 if intValue is not None else defaultParam}"
                    )
                    return (
                        intValue is not None and intValue != 0
                        if intValue is not None
                        else defaultParam
                    )
                else:
                    print(
                        f"Returning value: {iniSection2._variableValue if iniSection2._variableValue is not None else defaultParam}"
                    )
                    return (
                        iniSection2._variableValue
                        if iniSection2._variableValue is not None
                        else defaultParam
                    )
        print(f"Section or variable not found. Setting default value: {defaultParam}")
        self.setValue(section, variable, defaultParam)
        return defaultParam

    def setValue(self, section, variable, newValue):
        print(
            f"Entering setValue for section: {section}, variable: {variable}, newValue: {newValue}"
        )
        self._dirty = True
        iniSection = self.findSection(section)
        if iniSection is None:
            new_section = IniSection(section, None)
            print(f"Creating new section: {section}")
            if not self._head:
                self._head = new_section
                self._tail = new_section
                print(f"Setting _head and _tail to new section: {section}")
            else:
                self._tail._next = new_section
                new_section._prev = self._tail
                self._tail = new_section
                print(f"Linked new section: {section} to existing structure")
            iniSection = new_section
        iniSection2 = self.findVariable(iniSection, variable)
        if isinstance(newValue, int):
            if iniSection2 is None:
                iniSection2 = iniSection.addChild(variable, str(newValue))
                print(f"Created new variable: {variable} with int value")
            iniSection2.setIntValue(newValue)
        elif isinstance(newValue, float):
            if iniSection2 is None:
                iniSection2 = iniSection.addChild(variable, str(newValue))
                print(f"Created new variable: {variable} with float value")
            iniSection2.setFloatValue(newValue)
        elif isinstance(newValue, bool):
            if iniSection2 is None:
                iniSection2 = iniSection.addChild(variable, str(int(newValue)))
                print(f"Created new variable: {variable} with bool value")
            iniSection2.setIntValue(1 if newValue else 0)
        else:
            if iniSection2 is None:
                iniSection.addChild(variable, newValue)
                print(f"Created new variable: {variable} with string value")
            else:
                iniSection2._variableValue = newValue
                print(f"Updated existing variable: {variable} with string value")
        print(f"setValue completed successfully")
        return 1

    def findSection(self, section):
        current = self._head
        print(f"Starting to find section: {section} from _head")
        while current:
            if current._variableName == section:
                print(f"Found section: {section}")
                return current
            current = current._next
            print(
                f"Moving to next section: {current._variableName if current else None}"
            )
        print(f"Section {section} not found")
        return None

    def findVariable(self, section, variable):
        if section:
            current = section._childHead
            print(
                f"Starting to find variable: {variable} in section: {section._variableName}"
            )
            while current:
                if current._variableName == variable:
                    print(
                        f"Found variable: {variable} in section: {section._variableName}"
                    )
                    return current
                current = current._next
                print(
                    f"Moving to next variable: {current._variableName if current else None} in section: {section._variableName}"
                )
        print(
            f"Variable {variable} not found in section: {section._variableName if section else 'None'}"
        )
        return None

    def clear(self):
        if not self.root_created:
            self._head = IniSection("Root", None)
            self._tail = self._head
            self.root_created = True

    def construct(self, filename):
        self._dirty = False
        self.clear()
        try:
            with open(filename, "r") as sr:
                self.readFromFile(sr)
        except FileNotFoundError:
            pass

    def readFromFile(self, sr):
        current_section = self._head
        for line in sr:
            line = line.strip()
            section_match = IniSection.RegexSectionDefine.match(line)
            if section_match:
                section_name = section_match.group(1)
                new_section = self.findSection(section_name)
                if not new_section:
                    new_section = IniSection(section_name, None)
                    self._tail._next = new_section
                    new_section._prev = self._tail
                    self._tail = new_section
                current_section = new_section
            else:
                variable_match = IniSection.RegexVariable.match(line)
                if variable_match:
                    variable_name = variable_match.group(1)
                    variable_value = variable_match.group(2)
                    current_section.addChild(variable_name, variable_value)
        return True

    def writeToFile(self, sw):
        current = self._head
        while current:
            print(f"Writing section: {current._variableName}")
            current.writeSection(sw)
            current = current._next
        return True


if __name__ == "__main__":
    DEBUG = True
    test = IniFile("test.ini")
    test.getValue("Test1", "Test2", "WryIsAMaleGirl")
    test.setValue("Test1", "Test2", "MaleGirlYYDS")
    with open("test.ini", "w+") as f:
        test.writeToFile(f)
        f.flush()
    print(test.getValue("Test1", "Test2", "None"))
