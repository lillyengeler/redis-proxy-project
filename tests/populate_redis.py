from init_testing_struct import InitTestStruct

# populates redis instance with key/values so it can be tested by end user
def main():
    testEngine = InitTestStruct()
    testEngine.populate_redis({
        'name': 'lilly', 
        'color': 'blue', 
        'one': 'two', 
        'a':'b',
        'five':'six'
    })
    print("****************************************************************\n"
          "***                                                          ***\n"
          "**                       Tests Completed                      **\n"
          "*                                                              *\n"
          "*                      Enter Proxy Service:                    *\n"
          "*                                                              *\n"
          "*                     http://127.0.0.1:5000/                   *\n"  
          "*                                                              *\n"
          "**                                                            **\n"
          "***                                                          ***\n"
          "****************************************************************\n")


if __name__ == '__main__':
    main()