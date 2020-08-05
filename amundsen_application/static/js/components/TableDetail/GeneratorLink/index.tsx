import * as React from 'react';

import { logClick } from 'ducks/utilMethods';
import AvatarLabel from 'components/common/AvatarLabel';
import { TableGenerator } from 'interfaces';

export interface GeneratorLinkProps {
  tableGenerator: TableGenerator;
}

const GeneratorLink: React.SFC<GeneratorLinkProps> = ({
  tableGenerator,
}: GeneratorLinkProps) => {
  if (tableGenerator === null || tableGenerator.generator === null) return null;

  const image =
    tableGenerator.generator_type === 'airflow'
      ? '/static/images/airflow.jpeg'
      : '';
  return (
    <a
      className="header-link"
      href={tableGenerator.generator}
      id="explore-generator"
      onClick={logClick}
      target="_blank"
      rel="noreferrer"
    >
      <AvatarLabel label={tableGenerator.generator_type} src={image} />
    </a>
  );
};

export default GeneratorLink;
