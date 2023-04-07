When you generate a database with `goodcrap` and plan to fill it, you can either fill it using the default filler `GoodCrap.run()`, or you can generate a `Mage` integration pipeline using `GoodCrap.generate_pipeline()`.

The `Mage` project is generated using the command `mage init <project>`. Once the pipeline code is generated, the user can start the project using `mage start <project>`.

Each table is filled using a separate `Mage` pipeline.

The python codes are generated using the Jinja templates, and then written into the `Mage` project files.