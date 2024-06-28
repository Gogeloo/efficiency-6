# Efficiency 6

**Efficiency 6** is an open-source project developed by [Gogeloo](https://github.com/Gogeloo), aimed at enhancing the integration and control of computers within the popular sandbox game Minecraft. This project utilizes the powerful CCTweaked mod, previously known as ComputerCraft, to provide an API that allows players to interact with in-game computers using the Lua programming language. Additionally, the project leverages Advanced Peripherals to extend the capabilities and functionalities of these computers.

## Key Features

1. **Retrieving Raw Lua Files**: One of Efficiency 6's features is the ability to fetch raw Lua files. This functionality enables users to access and manipulate Lua scripts directly, improving the programming process and automating tasks within Minecraft. By providing raw access, Efficiency 6 gives users full control over their scripts and can implement custom solutions quickly.

2. **Posting Lua Files**: Efficiency 6 supports POST requests to temporarily save Lua files on the server. This feature allows for quick testing and iteration of scripts. If a script needs to be stored longer, users can commit the Lua files as a pull request (PR) to the Efficiency 6 project repository.

## Project Structure

Efficiency 6 is designed with a modular and extensible architecture, allowing integration with existing systems and future expansions. The project structure is organized to be easy to use, maintain, and collaborate among developers. Here’s a brief overview of the general structure:

1. **API Module**: The core of Efficiency 6 is the API module, which provides functions and methods for interacting with in-game computers. This module abstracts the complexities of the underlying CCTweaked and Advanced Peripherals, offering a user-friendly interface for developers.

2. **Lua File Handler**: This component manages the retrieval and manipulation of raw Lua files. It includes functions for reading, writing, and executing Lua scripts, making it an important part of the project’s functionality.

3. **Peripheral Integration**: Leveraging the Advanced Peripherals mod, this module extends the capabilities of the in-game computers by integrating various peripherals. This allows for more complex and sophisticated automation setups and makes CCTweaked capable of performing tasks it could not do before.

4. **Documentation and Examples**: The project includes documentation and a collection of example scripts to help developers get started with Efficiency 6. These resources provide instructions and practical examples, helping users quickly grasp the concepts and build their own automated systems.

## API Documentation

Efficiency 6 follows the [OPENAPI](https://arvidberndtsson.com/the-openapi-standard/) standard for API documentation. This ensures our API is well-documented, consistent, and easy to understand. Users can access detailed information about each endpoint, including request and response formats, parameters, and example usage. The OPENAPI documentation helps developers to integrate and use an API more efficiently, reducing the learning curve and improving overall productivity.

## Vision and Future Development

Efficiency 6 aims to be a cool project for nerds who want to learn more about automation and programming in LUA while playing Minecraft.

### Future plan
[] **Enhanced Documentation**: Expanding the documentation to cover more advanced topics and use cases, ensuring that users can fully exploit the capabilities of the API.
[] **Community Contributions**: Encouraging contributions from the community to add new features, improve existing functionality, and fix bugs.

## License

Efficiency 6 is released under the MIT License. For more information, please refer to the [LICENSE](LICENSE) file in the project repository.
