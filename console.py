#!/usr/bin/python3
<<<<<<< HEAD
"""Defines the HBnB console."""
import cmd
import re
from shlex import split
from models import storage
from models.base_model import BaseModel
from models.user import User
from models.state import State
from models.city import City
from models.place import Place
from models.amenity import Amenity
from models.review import Review


def parse(arg):
    curly_braces = re.search(r"\{(.*?)\}", arg)
    brackets = re.search(r"\[(.*?)\]", arg)
    if curly_braces is None:
        if brackets is None:
            return [i.strip(",") for i in split(arg)]
        else:
            lexer = split(arg[:brackets.span()[0]])
            retl = [i.strip(",") for i in lexer]
            retl.append(brackets.group())
            return retl
    else:
        lexer = split(arg[:curly_braces.span()[0]])
        retl = [i.strip(",") for i in lexer]
        retl.append(curly_braces.group())
        return retl


class HBNBCommand(cmd.Cmd):
    """Defines the HolbertonBnB command interpreter.

    Attributes:
        prompt (str): The command prompt.
    """

    prompt = "(hbnb) "
    __classes = {
        "BaseModel",
        "User",
        "State",
        "City",
        "Place",
        "Amenity",
        "Review"
    }

    def emptyline(self):
        """Do nothing upon receiving an empty line."""
        pass

    def default(self, arg):
        """Default behavior for cmd module when input is invalid"""
        argdict = {
            "all": self.do_all,
            "show": self.do_show,
            "destroy": self.do_destroy,
            "count": self.do_count,
            "update": self.do_update
        }
        match = re.search(r"\.", arg)
        if match is not None:
            argl = [arg[:match.span()[0]], arg[match.span()[1]:]]
            match = re.search(r"\((.*?)\)", argl[1])
            if match is not None:
                command = [argl[1][:match.span()[0]], match.group()[1:-1]]
                if command[0] in argdict.keys():
                    call = "{} {}".format(argl[0], command[1])
                    return argdict[command[0]](call)
        print("*** Unknown syntax: {}".format(arg))
        return False

    def do_quit(self, arg):
        """Quit command to exit the program."""
        return True

    def do_EOF(self, arg):
        """EOF signal to exit the program."""
        print("")
        return True

    def do_create(self, arg):
        """Usage: create <class>
        Create a new class instance and print its id.
        """
        argl = parse(arg)
        if len(argl) == 0:
            print("** class name missing **")
        elif argl[0] not in HBNBCommand.__classes:
            print("** class doesn't exist **")
        else:
            print(eval(argl[0])().id)
            storage.save()

    def do_show(self, arg):
        """Usage: show <class> <id> or <class>.show(<id>)
        Display the string representation of a class instance of a given id.
        """
        argl = parse(arg)
        objdict = storage.all()
        if len(argl) == 0:
            print("** class name missing **")
        elif argl[0] not in HBNBCommand.__classes:
            print("** class doesn't exist **")
        elif len(argl) == 1:
            print("** instance id missing **")
        elif "{}.{}".format(argl[0], argl[1]) not in objdict:
            print("** no instance found **")
        else:
            print(objdict["{}.{}".format(argl[0], argl[1])])

    def do_destroy(self, arg):
        """Usage: destroy <class> <id> or <class>.destroy(<id>)
        Delete a class instance of a given id."""
        argl = parse(arg)
        objdict = storage.all()
        if len(argl) == 0:
            print("** class name missing **")
        elif argl[0] not in HBNBCommand.__classes:
            print("** class doesn't exist **")
        elif len(argl) == 1:
            print("** instance id missing **")
        elif "{}.{}".format(argl[0], argl[1]) not in objdict.keys():
            print("** no instance found **")
        else:
            del objdict["{}.{}".format(argl[0], argl[1])]
            storage.save()

    def do_all(self, arg):
        """Usage: all or all <class> or <class>.all()
        Display string representations of all instances of a given class.
        If no class is specified, displays all instantiated objects."""
        argl = parse(arg)
        if len(argl) > 0 and argl[0] not in HBNBCommand.__classes:
            print("** class doesn't exist **")
        else:
            objl = []
            for obj in storage.all().values():
                if len(argl) > 0 and argl[0] == obj.__class__.__name__:
                    objl.append(obj.__str__())
                elif len(argl) == 0:
                    objl.append(obj.__str__())
            print(objl)

    def do_count(self, arg):
        """Usage: count <class> or <class>.count()
        Retrieve the number of instances of a given class."""
        argl = parse(arg)
        count = 0
        for obj in storage.all().values():
            if argl[0] == obj.__class__.__name__:
                count += 1
        print(count)

    def do_update(self, arg):
        """Usage: update <class> <id> <attribute_name> <attribute_value> or
       <class>.update(<id>, <attribute_name>, <attribute_value>) or
       <class>.update(<id>, <dictionary>)
        Update a class instance of a given id by adding or updating
        a given attribute key/value pair or dictionary."""
        argl = parse(arg)
        objdict = storage.all()

        if len(argl) == 0:
            print("** class name missing **")
            return False
        if argl[0] not in HBNBCommand.__classes:
            print("** class doesn't exist **")
            return False
        if len(argl) == 1:
            print("** instance id missing **")
            return False
        if "{}.{}".format(argl[0], argl[1]) not in objdict.keys():
            print("** no instance found **")
            return False
        if len(argl) == 2:
            print("** attribute name missing **")
            return False
        if len(argl) == 3:
            try:
                type(eval(argl[2])) != dict
            except NameError:
                print("** value missing **")
                return False

        if len(argl) == 4:
            obj = objdict["{}.{}".format(argl[0], argl[1])]
            if argl[2] in obj.__class__.__dict__.keys():
                valtype = type(obj.__class__.__dict__[argl[2]])
                obj.__dict__[argl[2]] = valtype(argl[3])
            else:
                obj.__dict__[argl[2]] = argl[3]
        elif type(eval(argl[2])) == dict:
            obj = objdict["{}.{}".format(argl[0], argl[1])]
            for k, v in eval(argl[2]).items():
                if (k in obj.__class__.__dict__.keys() and
                        type(obj.__class__.__dict__[k]) in {str, int, float}):
                    valtype = type(obj.__class__.__dict__[k])
                    obj.__dict__[k] = valtype(v)
                else:
                    obj.__dict__[k] = v
        storage.save()


if __name__ == "__main__":
=======
"""
    This is the Air bnb clone Console. It works to navigate the
    Air bnb Environmet.
    Much like a shell.
"""
import re
import cmd
import models
from datetime import datetime


def pattern(arg):
    """ Changing the default input function to manage callable functions """
    pattern = '\.([^.]+)\(|([^(),]+)[,\s()]*[,\s()]*'
    argum = re.findall(pattern, arg)
    cmd = argum[0][0]
    argum = argum[1:]
    line = ' '.join(map(lambda x: x[1].strip('"'), argum))
    return cmd, line


def loop_dict(line, obj_update):
    """ looping function for the adv tasks"""
    idx = 4
    while idx <= len(line):
        try:
            attr = line[idx]
        except IndexError:
            print("** attribute name missing **")
        else:
            try:
                val = line[idx + 1]
            except IndexError:
                print("** no value found **")
            else:
                setattr(obj_update, attr, val)
                obj_update.save()
                if idx + 1 == len(line) - 1:
                    break
        idx += 1


class HBNBCommand(cmd.Cmd):
    """ Base Command file class """

    prompt = '(hbnb) '

    def do_create(self, argv):
        """ Creates a new object based on BaseModel """
        if len(argv) == 0:
            print("** class name missing **")
        else:
            try:
                cls = models.class_dict[argv]
            except KeyError:
                print("** class doesn't exist **")
            else:
                new_obj = cls()
                new_obj.save()
                print(new_obj.id)

    def do_show(self, argv):
        """ Prints the string representation of an instance
        given the class name and id """
        if len(argv) == 0:
            print("** class name missing **")
        else:
            line = argv.split()
            if line[0] in models.class_dict:
                try:
                    key = line[0] + '.' + line[1]
                except IndexError:
                    print("** instance id missing **")
                else:
                    try:
                        print(models.storage.all()[key])
                    except KeyError:
                        print("** no instance found **")
            else:
                print("** class doesn't exist **")

    def do_destroy(self, argv):
        """ Destroys an instances given the class name & id """
        if len(argv) == 0:
            return print("** class name missing **")
        else:
            line = argv.split()
            if line[0] in models.class_dict:
                try:
                    key = line[0] + '.' + line[1]
                except IndexError:
                    print("** instance id missing **")
                else:
                    try:
                        del models.storage.all()[key]
                    except KeyError:
                        print("** no instance found **")
                    else:
                        models.storage.save()
            else:
                print("** class doesn't exist **")

    def do_all(self, line):
        """rints all string representation of all instances
        based or not on the class name"""
        if len(line) == 0:
            print([str(v) for v in models.storage.all().values()])
        elif line not in models.class_dict:
            print("** class doesn't exist **")
        else:
            print([str(v) for k, v in models.storage.all().items()
                   if line in k])

    def do_update(self, line):
        """pdates an instance based on the class name and id by
        adding or updating attribute"""
        if len(line) == 0:
            print("** class name missing **")
        else:
            line = line.split(' ')
            for i in range(len(line)):
                line[i] = line[i].strip("\"'\"{\"}:\"'")
            if line[0] in models.class_dict:
                try:
                    obj_id = line[0] + '.' + line[1]
                except IndexError:
                    print("** instance id missing **")
                else:
                    try:
                        obj = models.storage.all()[obj_id]
                    except KeyError:
                        print("** no instance found **")
                    else:
                        try:
                            attr = line[2]
                        except IndexError:
                            print("** attribute name missing **")
                        else:
                            try:
                                val = line[3]
                            except IndexError:
                                print("** value missing **")
                            else:
                                setattr(obj, attr, val)
                                obj.save()
                                if len(line) >= 5:
                                    loop_dict(line, obj)
            else:
                print("** class doesn't exist **")

    def do_count(self, line):
        """ Counts the number of instances of a class """
        instance_cnt = 0
        curr_dict = models.storage.all()
        for key, val in curr_dict.items():
            val = val.to_dict()
            if val['__class__'] == line:
                instance_cnt += 1
        print(instance_cnt)

    def do_Amenity(self, arg):
        """ helper function for amenity class """
        cmd, line = pattern(arg)
        self.onecmd(' '.join([cmd, 'Amenity', line]))

    def do_User(self, arg):
        """ Helper function for User class """
        cmd, line = pattern(arg)
        self.onecmd(' '.join([cmd, 'User', line]))

    def do_BaseModel(self, arg):
        """ Helper function for BaseModel Class """
        cmd, line = pattern(arg)
        self.onecmd(' '.join([cmd, 'BaseModel', line]))

    def do_City(self, arg):
        """ Helper function for BaseModel Class """
        cmd, line = pattern(arg)
        self.onecmd(' '.join([cmd, 'City', line]))

    def do_Review(self, arg):
        """ Helper function for Review class """
        cmd, line = pattern(arg)
        self.onecmd(' '.join([cmd, 'Review', line]))

    def do_State(self, arg):
        """ Helper function for State class """
        cmd, line = pattern(arg)
        self.onecmd(' '.join([cmd, 'State', line]))

    def do_Place(self, arg):
        """ Helper function for Place class"""
        cmd, line = pattern(arg)
        self.onecmd(' '.join([cmd, 'Place', line]))

    def emptyline(self):
        """ Does nothing on (empty line + 'Enter') """
        pass

    def do_quit(self, line):
        """ --- quit help documentation ---
        The quit function closes the console gracefully """
        return True

    def do_EOF(self, line):
        """ --- EOF help documentation ---
        EOF force closes the console.
        Use (Ctrl + D) to force close the console. """
        print()
        return True

if __name__ == '__main__':
>>>>>>> Giddy
    HBNBCommand().cmdloop()
