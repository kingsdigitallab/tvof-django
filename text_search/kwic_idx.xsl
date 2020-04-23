<xsl:stylesheet version="1.0"
 xmlns:xsl="http://www.w3.org/1999/XSL/Transform">
  <xsl:output omit-xml-declaration="no" indent="yes" encoding="utf-8"/>
  <!-- xsl:strip-space elements="*"/ -->

  <xsl:template match="kwiclist">
    <kwicindex>
      <xsl:apply-templates select=".//item">
        <xsl:sort select="@location" />
        <xsl:sort select="number(@n)" data-type="number" />
      </xsl:apply-templates>
    </kwicindex>
  </xsl:template>


  <xsl:template match="node()|@*">
    <xsl:copy>
      <xsl:apply-templates select="node()|@*"/>
    </xsl:copy>
  </xsl:template>

</xsl:stylesheet>
