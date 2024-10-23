import os
from typing import Callable


def clear_console():
    # Clear the console based on the operating system
    if os.name == 'nt':  # For Windows
        os.system('cls')
    else:  # For Linux/macOS
        os.system('clear')


class InvalidInputException(Exception):
    pass


class MenuCallable:
    input_options: list[str]
    func_call: Callable
    request_input: dict
    print_result: bool
    additional_params: dict

    def __init__(
        self,
        input_options: list[str],
        func_call: Callable = None,
        request_input: dict = None,
        print_result: bool = False,
        additional_params: dict = None
    ):
        """
        Generates a function call if the given input matches input_options.
        If the function called by func_call requires input parameters, you can ask them through request_input.
        :param input_options: List of options that lead to this call. For example, if the user inputs 1 and input_options contains 1, it will call func_call
        :param func_call: The function that will be called if the user inputs an option in input_options. This must be a reference to the function.
        :param request_input: A dictionary containing further input requests that will be sent as parameters to your function. The keys of this dictionary will be the function parameter name, and the values will be the message prompted to ask for the parameter value. Example: {'name': "Input your name"}
        :param print_result: If true, the result of the function call will be printed.
        :param additional_params: Any other parameters to be sent to func_call that are not directly requested through request_input.
        """
        self.input_options = input_options
        self.func_call = func_call
        self.request_input = request_input
        self.print_result = print_result
        self.additional_params = additional_params

    def __call__(self, *args, **kwargs):
        if not self.func_call:
            return
        inputs = self.additional_params if self.additional_params else {}
        if self.request_input:
            for key, value in self.request_input.items():
                response = input(f"{value}\n")
                inputs[key] = response
        result = self.func_call(**inputs)
        if self.print_result:
            print(result)


class Option:
    option_message: str
    menu_callable: MenuCallable

    def __init__(self, option_message: str, menu_callable: MenuCallable = None):
        """
        This class represents a single option in a menu. You can add a message for each option, and the function that will be called if the user chooses the option.
        :param option_message: The text to show that represents this option.
        :param menu_callable: A MenuCallable object that will be called if the option is chosen.
        """
        self.option_message = option_message
        self.menu_callable = menu_callable

    def __call__(self, input_option: str, *args, **kwargs):
        print(self.option_message)
        self.menu_callable(input_option, **kwargs)


class Submenu:
    pass


class Menu:
    main_text: list[str]
    options: list[Option]
    reshow_on_exception: bool
    loop_menu: bool
    clear_on_loop: bool
    custom_exception_message: str
    raise_on_invalid_option: bool
    expects_input: bool
    exit_option: Option

    def __init__(
        self,
        main_text: list[str],
        expects_input: bool,
        options: list[Option] = None,
        raise_on_invalid_option: bool = True,
        reshow_on_exception: bool = True,
        custom_exception_message: str = None,
        exit_option: Option = None,
        loop_menu: bool = False,
        clear_on_loop: bool = True
    ):
        """
        Shows an interactable console menu that the user can interact with. You can add as many Options as you want.
        See Option and MenuCallable for more information on how to call functions and add options to this menu.
        :param main_text: Lines of text that will be shown when the menu is called.
        :param expects_input: If true, the menu will expect a user input.
        :param options: If expects_input, the options that the user can choose from. They must be instances of Option with a MenuCallable.
        :param raise_on_invalid_option: If true, an exception will show if the users chooses an invalid option.
        :param reshow_on_exception: If true, the menu will be shown again if there's an exception during the MenuCallable function call.
        :param custom_exception_message: If true, the message that will be shown if there's an exception during the MenuCallable function call. If false, the raised exception message will be printed instead.
        :param exit_option: The Option object that represents the option that exits the menu. The MenuCallable in this Option may not have any func_call attached to it.
        :param loop_menu: If true, the menu will be shown again after an option is completed.
        :param clear_on_loop: If true, the console will be cleared after a loop. Requires loop_menu to be true.
        """
        self.main_text = main_text
        self.options = options
        self.expects_input = expects_input
        self.raise_on_invalid_option = raise_on_invalid_option
        self.reshow_on_exception = reshow_on_exception
        self.custom_exception_message = custom_exception_message
        self.exit_option = exit_option
        self.loop_menu = loop_menu
        self.clear_on_loop = clear_on_loop

    def __call__(self, *args, **kwargs):
        for text in self.main_text:
            print(text)
        if not self.expects_input:
            return

        for option in self.options:
            print(option.option_message)
        print(self.exit_option.option_message)
        response = input()
        if response in self.exit_option.menu_callable.input_options:
            self.exit_option.menu_callable()
            return

        valid_input = False
        try:
            for option in self.options:
                if response in option.menu_callable.input_options:
                    valid_input = True
                    option.menu_callable()
        except Exception as e:
            if self.custom_exception_message:
                print(self.custom_exception_message)
            else:
                print(str(e))
            if self.reshow_on_exception:
                self.__call__(*args, **kwargs)
                return

        if not valid_input and self.raise_on_invalid_option:
            raise InvalidInputException("The given input is invalid")
        elif self.loop_menu:
            if self.clear_on_loop:
                clear_console()
            print()
            self.__call__(*args, **kwargs)



